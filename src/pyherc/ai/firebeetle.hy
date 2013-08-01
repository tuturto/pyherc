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

(setv __doc__ "module for AI routines for firebeetles")

(import [pyherc.aspects [logged]]
	[pyherc.ai.pathfinding [a-star]]
	[pyherc.ai.common [patrol close-in-enemy fight-in-melee]]
	[pyherc.ai.common [select-patrol-area patrollable-area-in-level]]
	[pyherc.ai.common [move-towards-patrol-area get-random-patrol-direction]]
	[pyherc.ai.basic [can-walk? walk wait distance-between find-direction]]
	[pyherc.ai.basic [map-direction direction-mapping]]
	[pyherc.events [NoticeEvent]]
	[random]
	[math [sqrt]]
	[functools [partial]])

(require pyherc.ai.macros)

(defclass FireBeetleAI []
  [[__doc__ "AI routine for fire beetles"]
   [character None]
   [mode [:find-room None]]
   [--init-- (fn [self character]
	       "default constructor"
	       (.--init-- (super FireBeetleAI self))
	       (setv self.character character) None)]
   [act (fn [self model action-factory rng] 
	  "check the situation and act accordingly"
	  (beetle-act self model action-factory))]])

(with-decorator logged 
  (defn beetle-act [ai model action-factory]
    "main routine for beetle AI"
    (if (not (= (first ai.mode) :fight))
      (let [[enemy (enemy-close? ai)]]
	(if enemy (start-fighting ai enemy))))
    (let [[func (get mode-bindings (first ai.mode))]]
      (func ai action-factory))))

(defn is-open-space? [level x y]
  "check if given location is within patrol area"
  (and (not (.blocks-movement level (+ x 1) y))
       (not (.blocks-movement level (- x 1) y))
       (not (.blocks-movement level x (+ y 1)))
       (not (.blocks-movement level x (- y 1)))
       (not (.blocks-movement level (+ x 1) (+ y 1)))
       (not (.blocks-movement level (+ x 1) (- y 1)))
       (not (.blocks-movement level (- x 1) (+ y 1)))
       (not (.blocks-movement level (- x 1) (- y 1)))))

; move this to common
(with-decorator logged
  (defn find-open-space [ai action-factory]
    "routine to make character to find an open space"
    (if (is-open-space? ai.character.level
			(first ai.character.location)
			(second ai.character.location))
      (do (start-patrolling-room ai)
	  (patrol-room ai action-factory))
      (if (second ai.mode)
	(move-towards-patrol-area ai action-factory)
	(select-room-to-patrol ai)))))

(defn attack [ai enemy action-factory rng]
  "attack an enemy"
  (let [[attacker ai.character]
	[attacker-location attacker.location]
	[target-location enemy.location]	
	[attack-direction (map-direction (find-direction attacker-location 
							 target-location))]]
    (.perform-attack attacker attack-direction action-factory rng)))

(defn enemy-close? [ai]
  "check if there is an enemy close by, returns preferred enemy"
  (let [[level ai.character.level]
	[player ai.character.model.player]]
    (if (< (distance-between player.location ai.character.location) 4)
      player)))

(defn start-fighting [ai enemy]
  "pick start fighting again enemy"
  (focus-enemy ai enemy)
  (setv ai.mode [:fight
		enemy]))

(defn start-patrolling-room [ai]
  (let [[patrol-direction random-patrol-direction]]
    (if patrol-direction
      (setv ai.mode [:patrol-room
		     (patrol-direction ai)])
      (wait ai))))

(defn focus-enemy [ai enemy]
  "focus on enemy and start tracking it"
  (let [[character ai.character]
	[event (NoticeEvent character enemy)]]
    (.raise-event character event)))

(def random-patrol-direction (partial get-random-patrol-direction is-open-space?))

(def close-in (partial close-in-enemy 
		       (fn [start end level] (first (a-star start
							    end 
							    level)))))
(def fight (partial fight-in-melee attack close-in))

(def open-space (partial patrollable-area-in-level is-open-space?))

(def select-room-to-patrol (partial select-patrol-area open-space))

(def patrol-room (partial patrol is-open-space? start-patrolling-room))

(def mode-bindings {:find-room find-open-space
		    :patrol-room patrol-room
		    :fight fight})


