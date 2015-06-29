;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2015 Tuukka Turto
;;
;;  This file is part of pyherc.
;;
;;  pyherc is free software: you can redistribute it and/or modify
;;  it under the terms of the GNU General Public License as published by
;;  the Free Software Foundation, either version 3 of the License, or
;;  (at your option) any later version.
;;
;;  pyherc is distributed in the hope that it will be useful,
;;  but WITHOUT ANY WARRANTY; without even the implied warranty of
;;  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;  GNU General Public License for more details.
;;
;;  You should have received a copy of the GNU General Public License
;;  along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

(require pyherc.macros)

(import [hamcrest [assert-that is- equal-to has-item]]
        [mockito [mock verify verifyNoMoreInteractions]])
(import [pyherc.test.builders [ActionFactoryBuilder CharacterBuilder
                               LevelBuilder]]
        [pyherc.test.matchers [EventType]])
(import [pyherc.data [add-visited-level]]
        [pyherc.data.new-character [visited-levels↜]]
        [pyherc.data.constants [Direction]]
        [pyherc.events [NewLevelEvent]]
        [pyherc.rules [move]])

(defn test-add-visited-level []
  "test that adding and retrieving a level in visited list is possible"
  (let [[character (-> (CharacterBuilder)
                       (.build))]]
    (add-visited-level character "crystal forest")
    (assert-that (visited-levels↜ character)
                 (has-item "crystal forest"))))

(defn test-same-level-added-only-once []
  "test that same level can be added only once"
  (let [[character (-> (CharacterBuilder)
                       (.build))]]
    (add-visited-level character "crystal forest")
    (add-visited-level character "crystal forest")
    (assert-that (len (list (visited-levels↜ character)))
                 (is- (equal-to 1)))))

(defn setup []
  "setup test case"
  (let [[listener (mock)]
        [level (-> (LevelBuilder)
                   (.build))]
        [character (-> (CharacterBuilder)
                       (.with-level level)
                       (.with-location #t(5 5))
                       (.with-update-listener listener)
                       (.build))]
        [actions (-> (ActionFactoryBuilder)
                     (.with-move-factory)
                     (.build))]]
    {:listener listener
     :level level
     :character character
     :actions actions}))

(defn test-event-raised []
  "moving to new level should raise new level event"
  (let [[context (setup)]
        [listener (:listener context)]
        [level (:level context)]
        [character (:character context)]
        [actions (:actions context)]]
    (move character Direction.north actions)
    (-> (verify listener)
        (.receive-update (EventType "new level")))))

(defn test-event-not-raised-for-old-level []
  "when player moves in an old level, no new level event should be raised"
  (let [[context (setup)]
        [listener (:listener context)]
        [level (:level context)]
        [character (:character context)]
        [actions (:actions context)]]
    (add-visited-level character level)
    (move character Direction.north actions)
    (-> (verify listener)
        (.receive-update (EventType "move")))
    (verifyNoMoreInteractions listener)))
