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

(require pyherc.macros)

(import [random]
        [pyherc.aspects [log-debug log-info]]
        [pyherc.data [get-portal blocks-movement get-character]]
        [pyherc.data.geometry [area-around]]
        [pyherc.rules.factory [SubActionFactory]]
        [pyherc.rules.moving.action [EscapeAction MoveAction FlyAction
                                     SwitchPlacesAction WalkAction]])

(defclass MoveFactory [SubActionFactory]
  "factory for creating movement actions"
  [[--init-- (fn [self level-generator-factory dying-rules]
               (super-init)
               (setv self.level-generator-factory level-generator-factory)
               (setv self.dying-rules dying-rules)
               (setv self.action-type "move")
               nil)]
   [--str-- (fn [self]
              "move factory")]
   [get-action (fn [self parameters]
                 "create movement action"
                 (let [[character parameters.character]
                       [location character.location]
                       [new-level character.level]
                       [direction parameters.direction]
                       [new-location nil]]
                   (if (= 9 direction)
                     (get-action-for-portal character
                                            self.level-generator-factory
                                            self.dying-rules)
                     (do
                      (setv new-location (.get-location-at-direction character direction))
                      (cond [(blocks-movement new-level new-location)
                             (if (= "walk" "walk")
                               (WalkAction :character character
                                           :new-location location
                                           :new-level new-level
                                           :skip-creature-check false
                                           :dying-rules self.dying-rules)
                               (FlyAction :character character
                                          :new-location location
                                          :new-level new-level
                                          :skip-creature-check false
                                          :dying-rules self.dying-rules))]
                            [(get-character new-level new-location)
                             (get-place-switch-action character
                                                      new-location
                                                      self.dying-rules)]
                            [true 
                             (if (= "walk" "walk")
                               (WalkAction :character character
                                           :new-location new-location
                                           :new-level new-level
                                           :skip-creature-check false
                                           :dying-rules self.dying-rules)
                               (FlyAction :character character
                                          :new-location new-location
                                          :new-level new-level
                                          :skip-creature-check false
                                          :dying-rules self.dying-rules))])))))]])

(defn get-place-switch-action [character new-location dying-rules]
  "get action for two characters switching places"
  (let [[other-character (get-character character.level new-location)]]
    (SwitchPlacesAction character
                        other-character
                        dying-rules)))

(defn get-action-for-portal [character level-generator-factory dying-rules]
  "get action for entering portal"
  (let [[location character.location]
        [level character.level]
        [portal (get-portal level location)]]
    (if portal
      (if portal.exits-dungeon
        (EscapeAction character)
        (let [[other-end (.get-other-end portal level-generator-factory)]]
          (MoveAction character
                      (landing-location other-end)
                      other-end.level
                      false
                      dying-rules)))
      (MoveAction character
                  location
                  level
                  false
                  dying-rules))))

(defn landing-location [portal]
  "get landing spot on or around a portal"
  (if (not (or (blocks-movement portal.level portal.location)
               (get-character portal.level portal.location)))
    portal.location
    (.choice random (list-comp x [x (area-around portal.location)]
                               (not (or (blocks-movement portal.level x)
                                        (get-character portal.level x)))))))
