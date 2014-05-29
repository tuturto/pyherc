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

(setv __doc__ "module for common AI routines")

(require pyherc.aspects)
(require pyherc.macros)
(import [pyherc.aspects [log_debug]]
    [pyherc.ai.pathfinding [a-star]]
    [pyherc.rules [is-move-legal]]
    [pyherc.data [find-direction get-tiles]]
    [herculeum.ai.basic [can-walk? walk wait distance-between new-location]]
    [herculeum.ai.basic [focus-enemy attack-enemy]]
    [random]
    [math [sqrt]]
    [functools [partial]])

(require herculeum.ai.macros)

#d(defn -fight-in-melee [attack-routine close-in-routine ai action-factory]
    "routine to make character to fight"
    (let [[own-location ai.character.location]
	  [enemy (second ai.mode)]
	  [enemy-location enemy.location]
	  [distance (distance-between own-location enemy-location)]]
      (if (= distance 1)
	(attack-routine ai enemy action-factory (.Random random))
	(close-in-routine ai enemy action-factory))))

#d(defn -close-in-enemy [routing-function ai enemy action-factory]
    "get closer to enemy"
    (let [[start-location ai.character.location]
	  [end-location enemy.location]
	  [path (routing-function start-location
				  end-location
				  ai.character.level)]]
      (walk ai action-factory (find-direction start-location (second path)))))

#d(defn -select-patrol-area [patrol-area-locator ai]
    (let [[patrol-area (patrol-area-locator ai.character.level)]
	  [target (.choice random patrol-area)]]
      (assoc ai.mode 1 target)))

#d(defn -patrol [is-patrol-area start-patrol ai action-factory]
    "routine to make character to patrol area"
    (assert (second ai.mode))
    (let [[future-location (new-location ai.character (second ai.mode))]]
      (often (if (and (can-walk? ai action-factory (second ai.mode))
		      (is-patrol-area ai.character.level future-location))
	       (walk ai action-factory)
	       (if (is-patrol-area ai.character.level ai.character.location)
		 (do (start-patrol ai)
		     (wait ai))
		 (-walk-random-direction ai action-factory)))
	     (wait ai))))

#d(defn -walk-random-direction [ai action-factory]
    "take a random step without changing mode"
    (let [[legal-directions (list-comp direction
				       [direction #t(1 3 5 7)]
				       (is-move-legal ai.character
						      direction
						      "walk"
						      action-factory))]]
      (if (len legal-directions) (assoc ai.mode 1
					(.choice random legal-directions))
	  (wait ai))))

#d(defn -find-patrol-area [is-patrollable start-patrolling patrol
			   move-towards-patrol-area select-patrol-area
			   ai action-factory]
    "routine to make character to find a patrol area"
    (if (is-patrollable ai.character.level ai.character.location)
      (do (start-patrolling ai)
	  (patrol ai action-factory))
      (if (second ai.mode)
	(move-towards-patrol-area ai action-factory)
	(select-patrol-area ai))))

#d(defn -patrollable-area-in-level [can-patrol level]
    "routine to find area to patrol in level"
    (let [[patrol-area []]]
      (for [#t(location tile) (get-tiles level)]
        (if (can-patrol level location)
          (.append patrol-area location)))
      patrol-area))

#d(defn -move-towards-patrol-area [select-area-to-patrol ai action-factory]
    (let [[start-location ai.character.location]
	  [path (first (a-star start-location
			       (second ai.mode)
			       ai.character.level))]]
      (if path
	(walk ai action-factory (find-direction start-location (second path)))
	(select-area-to-patrol ai))))

#d(defn -get-random-patrol-direction [is-patrollable ai]
    "select a random direction to follow"
    (let [[possible-directions []]
	  [character-x (first ai.character.location)]
	  [character-y (second ai.character.location)]
	  [level ai.character.level]]
      (for [offset [#t(0 1) #t(0 -1) #t(1 0) #t(-1 0)]]
	(let [[x (+ character-x (first offset))]
	      [y (+ character-y (second offset))]]
	  (if (is-patrollable level #t(x y))
	    (.append possible-directions #t(x y)))))
      (if possible-directions
	(find-direction ai.character.location (.choice random possible-directions))
	(wait ai))))

#d(defn -enemy-close? [max-distance ai]
    "check if there is an enemy close by, returns preferred enemy"
    (let [[level ai.character.level]
	  [player ai.character.model.player]]
      (if (< (distance-between player.location ai.character.location) max-distance)
	player)))

#d(defn -start-fighting [ai enemy]
    "start fighting against enemy"
    (focus-enemy ai enemy)
    (setv ai.mode [:fight
		   enemy]))

#d(defn -start-patrolling [get-random-patrol-direction ai]
    (setv ai.mode [:patrol
		   (get-random-patrol-direction ai)])
    (assert (second ai.mode)))

#d(defn patrol-ai [is-patrol-area detection-distance]
    "factory function for creating patrolling ai"
    (let [[enemy-close? (partial -enemy-close? detection-distance)]
	  [random-patrol-direction (partial -get-random-patrol-direction is-patrol-area)]
	  [patrol-space (partial -patrollable-area-in-level is-patrol-area)]
	  [select-area-to-patrol (partial -select-patrol-area patrol-space)]
	  [close-in (partial -close-in-enemy
			     (fn [start end level] (first (a-star start
								  end
								  level))))]
	  [fight (partial -fight-in-melee attack-enemy close-in)]
	  [patrol (partial -patrol is-patrol-area (partial -start-patrolling random-patrol-direction))]
	  [find-patrol-area (partial -find-patrol-area is-patrol-area (partial -start-patrolling random-patrol-direction)
				     patrol (partial -move-towards-patrol-area select-area-to-patrol)
				     select-area-to-patrol)]
	  [act (fn [transit patrol fight ai model action-factory]
		 "main routine for patrol AI"
		 (if (not (= (first ai.mode) :fight))
		   (let [[enemy (enemy-close? ai)]]
		     (if enemy (-start-fighting ai enemy))))
		 (cond
		  [(= (first ai.mode) :transit) (transit ai action-factory)]
		  [(= (first ai.mode) :patrol) (patrol ai action-factory)]
		  [(= (first ai.mode) :fight) (fight ai action-factory)]))]]
      (partial act find-patrol-area patrol fight)))
