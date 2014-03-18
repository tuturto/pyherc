;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2014 Tuukka Turto
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

(setv __doc__ "module for actions")

(import [pyherc.aspects [log_debug]]
    [pyherc.rules [move is-move-legal attack]]
    [pyherc.events [NoticeEvent]]
    [math [sqrt]])

(require herculeum.ai.macros)

(with-decorator log_debug
  (defn wait [ai]
    "make character to wait a little bit"
    (setv ai.character.tick 5)))

(defn can-walk? [ai action-factory direction]
  "check if character can walk to given direction"
  (is-move-legal ai.character direction "walk" action-factory))

(with-decorator log_debug
  (defn walk [ai action-factory &optional direction]
    "take a step to direction the ai is currently moving"
    (if direction
      (move ai.character direction action-factory)
      (move ai.character (second ai.mode) action-factory))))

(defn distance-between [start end]
  "calculate distance between two locations"
  (let [[dist-x (- (first start) (first end))]
    [dist-y (- (second start) (second end))]]
    (sqrt (+ (pow dist-x 2)
          (pow dist-y 2)))))

(defn find-direction [start destination]
  "calculate direction from start to destination"
  (assert (not (= start destination )))
  (let [[start-x (first start)]
    [start-y (second start)]
    [end-x (first destination)]
    [end-y (second destination)]]
    (if (= start-x end-x)
      (if (< start-y end-y) 5 1)
      (if (= start-y end-y)
    (if (< start-x end-x) 3 7)))))

(defn new-location [character direction]
  "get next location if going to given direction"
  (.get-location-at-direction character direction))

(defn attack-enemy [ai enemy action-factory rng]
  "attack an enemy"
  (let [[attacker ai.character]
    [attacker-location attacker.location]
    [target-location enemy.location]
    [attack-direction (find-direction attacker-location target-location)]]
    (attack attacker attack-direction action-factory rng)))

(defn focus-enemy [ai enemy]
  "focus on enemy and start tracking it"
  (let [[character ai.character]
    [event (NoticeEvent character enemy)]]
    (.raise-event character event)))
