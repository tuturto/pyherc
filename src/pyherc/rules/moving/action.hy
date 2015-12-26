;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2015 Tuukka Turto
;; 
;; Permission is hereby granted, free of charge, to any person obtaining a copy
;; of this software and associated documentation files (the "Software"), to deal
;; in the Software without restriction, including without limitation the rights
;; to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
;; copies of the Software, and to permit persons to whom the Software is
;; furnished to do so, subject to the following conditions:
;; 
;; The above copyright notice and this permission notice shall be included in
;; all copies or substantial portions of the Software.
;; 
;; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
;; IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
;; FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
;; AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
;; LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
;; OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
;; THE SOFTWARE.

(require hy.contrib.anaphoric)
(require pyherc.aspects)
(require pyherc.macros)
(require hymn.dsl)

(import [hymn.types.either [Left Right right?]]
        [pyherc.aspects [log-debug log-info]]
        [pyherc.data [blocks-movement get-character remove-character
                      add-character move-character add-visited-level
                      visited-levels speed-modifier]]
        [pyherc.data.constants [Duration]]
        [pyherc.data.level [traps↜]]
        [pyherc.data.geometry [find-direction]]
        [pyherc.data.model [*escaped-dungeon*]]
        [pyherc.events [new-move-event new-level-event]])

(defclass MoveAction []
  "action for moving"
  [[--init-- (fn [self character new-location new-level skip-creature-check
                  dying-rules]
               "default initializer"
               (super-init)
               (set-attributes character
                               new-location
                               new-level
                               skip-creature-check
                               dying-rules)
               nil)]
   [execute #i(fn [self]
                "execute this move"
                (if (.legal? self)
                  (let [[character self.character]
                        [old-location character.location]
                        [old-level character.level]
                        [direction (find-direction old-location self.new-location)]]
                    (move-character self.new-level
                                    self.new-location
                                    character)
                    (.add-to-tick character (/ Duration.fast (speed-modifier character)))
                    (when-not (in self.new-level (visited-levels character))
                              (add-visited-level character self.new-level)
                              (.raise-event character (new-level-event :character character
                                                                       :new-level self.new-level)))
                    (.raise-event character (new-move-event :character character
                                                            :old-location old-location
                                                            :old-level old-level
                                                            :direction direction))
                    (Right character))
                  (do (.add-to-tick self.character Duration.instant)
                      (Left character))))]
   [legal? #d(fn [self]
               "check if the move is possible to perform"
               (let [[level self.new-level]
                     [location self.new-location]]
                 (cond [(is level nil) false]
                       [(blocks-movement level location) false]
                       [(and (not self.skip-creature-check)
                             (get-character level location)) false]
                       [true true])))]
   [--str-- (fn [self]
              (.format "{0} at {1}:{2}" self.character self.new-location self.new-level))]])

(defclass WalkAction []
  "action for walking"  
  [[--init-- (fn [self character dying-rules base-action]
               "default initializer"
               (super-init)
               (set-attributes character dying-rules base-action)
               nil)]
   [legal? (fn [self]
             "check if the move is possible to perform"
             (.legal? self.base-action))]
   [execute #i(fn [self]
                "execute this move"
                (if (right? (.execute self.base-action))
                  (do (ap-each (traps↜ self.character.level self.character.location)
                           (.on-enter it self.character))
                      (.check-dying self.dying-rules self.character)
                      (Right self.character))
                  (Left self.character)))]])

(defclass FlyAction []
  "action for flying"
  [[--init-- (fn [self base-action]
               "default initializer"
               (super-init)
               (set-attributes base-action)
               nil)]
   [legal? (fn [self]
             "check if the move is possible to perform"
             (.legal? self.base-action))]
   [execute #i(fn [self]
                "execute this move"
                (.execute self.base-action))]])

(defclass EscapeAction []
  "action for escaping the dungeon"
  [[--init-- #d(fn [self character]
                 "default initializer"
                 (super-init)
                 (set-attributes character)
                 nil)]
   [execute #i(fn [self]
                "execute this move"
                (let [[model self.character.model]]
                  (setv model.end-condition *escaped-dungeon*))
                (Right self.character))]
   [legal? #d(fn [self]
               "check if move is possible to perform"
               (= self.character.model.player self.character))]])

(defclass SwitchPlacesAction []
  "action for switching places with another creature"
  [[--init-- #d(fn [self character other-character dying-rules]
                 "default initializer"
                 (super-init)
                 (set-attributes character other-character dying-rules)
                 (setv self.move-action₁ (WalkAction :character self.character
                                                     :dying-rules dying-rules
                                                     :base-action (MoveAction character
                                                                              self.other-character.location
                                                                              self.other-character.level
                                                                              true
                                                                              dying-rules)))
                 (setv self.move-action₂ (WalkAction :character self.other-character
                                                     :dying-rules dying-rules
                                                     :base-action (MoveAction self.other-character
                                                                              self.character.location
                                                                              self.character.level
                                                                              true
                                                                              dying-rules)))
                 nil)]
   [execute #i(fn [self]
                "execute this move"
                (if (.legal? self)
                  (let [[character₁ self.character]
                        [level₁ character₁.level]
                        [location₁ character₁.location]
                        [character₂ self.other-character]
                        [level₂ character₂.level]
                        [location₂ character₂.location]]
                    (remove-character level₂ character₂)
                    (.execute self.move-action₁)
                    (add-character level₁ location₁ character₂)
                    (.raise-event character₂ (new-move-event :character character₂
                                                             :old-location location₂
                                                             :old-level level₂
                                                             :direction (find-direction location₂
                                                                                        location₁)))
                    (ap-each (traps↜ level₂ location₂) (.on-enter character₂))
                    (.check-dying self.dying-rules character₂)
                    (Right character₁))
                  (do (.add-to-tick self.character Duration.instant)
                      (Left self.character))))]
   [legal? #d(fn [self]
               "check if this move is legal"
               (if (in self.character.model.player [self.character self.other-character])
                 false
                 (and (.legal? self.move-action₁)
                      (.legal? self.move-action₂))))]])
