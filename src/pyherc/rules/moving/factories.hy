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

(require pyherc.macros)

(import [random]
        [pyherc.aspects [log-debug log-info]]
        [pyherc.data [get-portal blocks-movement get-character movement-mode]]
        [pyherc.data.geometry [area-around]]
        [pyherc.rules.factory [SubActionFactory]]
        [pyherc.rules.moving.action [EscapeAction MoveAction FlyAction
                                     SwitchPlacesAction WalkAction]])

(defclass MoveFactory [SubActionFactory]
  "factory for creating movement actions"
  [[--init-- (fn [self level-generator-factory]
               (super-init)
               (setv self.level-generator-factory level-generator-factory)
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
                                            self.level-generator-factory)
                     (do
                      (setv new-location (.get-location-at-direction character direction))
                      (cond [(blocks-movement new-level new-location)
                             (if (= (movement-mode character) "walk")
                               (WalkAction :character character
                                           :base-action (MoveAction character
                                                                    location
                                                                    new-level
                                                                    false))
                               (FlyAction :base-action (MoveAction character
                                                                   location
                                                                   new-level
                                                                   false)))]
                            [(and (get-character new-level new-location)
                                  character.artificial-intelligence
                                  (. (get-character new-level new-location) artificial-intelligence))
                             (get-place-switch-action character
                                                      new-location)]
                            [true 
                             (if (= (movement-mode character) "walk")
                               (WalkAction :character character
                                           :base-action (MoveAction character
                                                                    new-location
                                                                    new-level
                                                                    false))
                               (FlyAction :base-action (MoveAction character
                                                                   new-location
                                                                   new-level
                                                                   false)))])))))]])

(defn get-place-switch-action [character new-location]
  "get action for two characters switching places"
  (let [[other-character (get-character character.level new-location)]]
    (SwitchPlacesAction character
                        other-character)))

(defn get-action-for-portal [character level-generator-factory]
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
                      false)))
      (MoveAction character
                  location
                  level
                  false))))

(defn landing-location [portal]
  "get landing spot on or around a portal"
  (if (not (or (blocks-movement portal.level portal.location)
               (get-character portal.level portal.location)))
    portal.location
    (.choice random (list-comp x [x (area-around portal.location)]
                               (not (or (blocks-movement portal.level x)
                                        (get-character portal.level x)))))))
