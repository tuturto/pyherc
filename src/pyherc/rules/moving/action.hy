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
(require pyherc.rules.macros)
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
        [pyherc.events [new-move-event new-level-event]]
        [pyherc])

(action-dsl)

(defaction move "action for moving"
  :parameters [character new-location new-level skip-creature-check]
  
  :legal-action (let [[character self.character]
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

  :illegal-action (do (.add-to-tick self.character Duration.instant)
                      (Left self.character))
  
  :legal? (none [(is (. self new-level) nil)
                 (blocks-movement (. self new-level) (. self new-location))
                 (and (not self.skip-creature-check)
                      (get-character (. self new-level) (. self new-location)))])

  
  :to-string (.format "{0} at {1}:{2}" self.character self.new-location self.new-level))

(defn trigger-traps [character]
  "trigger traps for character and check if they died"
  (ap-each (traps↜ (. character level) (. character location))
           (.on-enter it character))
  (call check-dying character)
  (Right character))

(defclass WalkAction []
  "action for walking"  
  [[--init-- (fn [self character base-action]
               "default initializer"
               (super-init)
               (set-attributes character base-action)
               nil)]
   [legal? (fn [self]
             "check if the move is possible to perform"
             (.legal? self.base-action))]
   [execute #i(fn [self]
                "execute this move"
                (if (right? (.execute self.base-action))
                  (trigger-traps self.character)
                  (Left self.character)))]])

(defaction escape "action for escaping the dungeon"
  :parameters [character]

  :legal-action (let [[model self.character.model]]
                  (setv model.end-condition *escaped-dungeon*)
                  (Right (. self character)))

  :illegal-action (Left (. self character))

  :legal? (= self.character.model.player self.character)
  
  :to-string (.format "{0} escaping dungeon" (. self character)))

(defclass SwitchPlacesAction []
  "action for switching places with another creature"
  [[--init-- #d(fn [self character other-character]
                 "default initializer"
                 (super-init)
                 (set-attributes character other-character)
                 (setv self.move-action₁ (WalkAction :character self.character                                                    
                                                     :base-action (MoveAction character
                                                                              self.other-character.location
                                                                              self.other-character.level
                                                                              true)))
                 (setv self.move-action₂ (WalkAction :character self.other-character
                                                     :base-action (MoveAction self.other-character
                                                                              self.character.location
                                                                              self.character.level
                                                                              true)))
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
                    (call check-dying character₂)
                    (Right character₁))
                  (do (.add-to-tick self.character Duration.instant)
                      (Left self.character₁))))]
   [legal? #d(fn [self]
               "check if this move is legal"
               (if (in self.character.model.player [self.character self.other-character])
                 false
                 (and (.legal? self.move-action₁)
                      (.legal? self.move-action₂))))]])
