;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2015 Tuukka Turto
;;
;;   This file is part of pyherc.
;;
;;   pyherc is free software: you can redistribute it and/or modify
;;   it under the terms of the GNU General Public License as published by
;;   the Free Software Foundation, either version 3 of the License, or
;;   (at your option) any later version.
;;
;;   pyherc is distributed in the hope that it will be useful,
;;   but WITHOUT ANY WARRANTY; without even the implied warranty of
;;   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;   GNU General Public License for more details.
;;
;;   You should have received a copy of the GNU General Public License
;;   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

(require hy.contrib.anaphoric)
(require pyherc.aspects)
(require pyherc.macros)

(import [pyherc.aspects [log-debug log-info]]
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
                                                            :direction direction)))
                  (.add-to-tick self.character Duration.instant))
                (ap-each (traps↜ self.character.level self.character.location)
                         (.on-enter it self.character))
                (.check-dying self.dying-rules self.character))]
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

(defclass WalkAction [MoveAction]
  "action for walking"
  [[execute #i(fn [self]
                "execute this move"
                (-> (super)
                    (.execute)))]])

(defclass EscapeAction [MoveAction]
  "action for escaping the dungeon"
  [[--init-- #d(fn [self character]
                 "default initializer"
                 (super-init :character character
                             :new-location nil
                             :new-level nil
                             :skip-creature-check false
                             :dying-rules nil)
                 nil)]
   [execute #i(fn [self]
                "execute this move"
                (let [[model self.character.model]]
                  (setv model.end-condition *escaped-dungeon*)))]
   [legal? #d(fn [self]
               "check if move is possible to perform"
               (= self.character.model.player self.character))]])

(defclass SwitchPlacesAction []
  "action for switching places with another creature"
  [[--init-- #d(fn [self character other-character dying-rules]
                 "default initializer"
                 (super-init)
                 (set-attributes character other-character dying-rules)
                 (setv self.move-action₁ (WalkAction self.character
                                                     self.other-character.location
                                                     self.other-character.level
                                                     true
                                                     dying-rules))
                 (setv self.move-action₂ (WalkAction self.other-character
                                                     self.character.location
                                                     self.character.level
                                                     true
                                                     dying-rules))
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
                    (.check-dying self.dying-rules character₂))
                  (.add-to-tick self.character Duration.instant)))]
   [legal? #d(fn [self]
               "check if this move is legal"
               (if (in self.character.model.player [self.character self.other-character])
                 false
                 (and (.legal? self.move-action₁)
                      (.legal? self.move-action₂))))]])
