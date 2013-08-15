;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2013 Tuukka Turto
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
	[pyherc.events [NoticeEvent]]
	[math [sqrt]])

(require pyherc.ai.macros)

(with-decorator log_debug
  (defn wait [ai]
    "make character to wait a little bit"
    (setv ai.character.tick 5)))

(defn can-walk? [ai action-factory direction]
  "check if character can walk to given direction"
  (.is-move-legal ai.character
		  (map-direction direction)
		  "walk"
		  action-factory))

(with-decorator log_debug
  (defn walk [ai action-factory &optional direction]
    "take a step to direction the ai is currently moving"
    (if direction
      (.move ai.character (map-direction direction) action-factory)
      (.move ai.character (map-direction (second ai.mode)) action-factory))))

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
      (if (< start-y end-y) :south :north)
      (if (= start-y end-y)
	(if (< start-x end-x) :east :west)
	(if (< start-y end-y)
	  (if (< start-x end-x) :south-east :south-west)
	  (if (< start-x end-x) :north-east :north-west))))))

(def direction-mapping {1 :north 2 :north-east 3 :east 4 :south-east 5 :south
			6 :south-west 7 :west 8 :north-west 9 :enter
			:north 1 :north-east 2 :east 3 :south-east 4 :south 5
			:south-west 6 :west 7 :north-west 8 :enter 9})

(defn map-direction [direction]
  "map between keyword and integer directions"
  (get direction-mapping direction))

(defn new-location [character direction]
  "get next location if going to given direction"
  (.get-location-at-direction character (map-direction direction)))

(defn attack [ai enemy action-factory rng]
  "attack an enemy"
  (let [[attacker ai.character]
	[attacker-location attacker.location]
	[target-location enemy.location]	
	[attack-direction (map-direction (find-direction attacker-location 
							 target-location))]]
    (.perform-attack attacker attack-direction action-factory rng)))

(defn focus-enemy [ai enemy]
  "focus on enemy and start tracking it"
  (let [[character ai.character]
	[event (NoticeEvent character enemy)]]
    (.raise-event character event)))
