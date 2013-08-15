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

(setv __doc__ "module for common AI routines")

(import [pyherc.aspects [log_debug]]
	[pyherc.ai.pathfinding [a-star]]
	[pyherc.ai.basic [can-walk? walk wait distance-between new-location]]
	[pyherc.ai.basic [find-direction]]
	[pyherc.ai.basic [focus-enemy attack]]
	[random]
	[math [sqrt]]
	[functools [partial]])

(require pyherc.ai.macros)

(with-decorator log_debug
  (defn -fight-in-melee [attack-routine close-in-routine ai action-factory]
    "routine to make character to fight"
    (let [[own-location ai.character.location]
	  [enemy (second ai.mode)]
	  [enemy-location enemy.location]
	  [distance (distance-between own-location enemy-location)]]
      (if (= distance 1)
	(attack-routine ai enemy action-factory (.Random random))
	(close-in-routine ai enemy action-factory)))))

(with-decorator log_debug
  (defn -close-in-enemy [routing-function ai enemy action-factory]
    "get closer to enemy"
    (let [[start-location ai.character.location]
	  [end-location enemy.location]
	  [path (routing-function start-location
				  end-location
				  ai.character.level)]]
      (walk ai action-factory (find-direction start-location (second path))))))

(with-decorator log_debug
  (defn -select-patrol-area [patrol-area-locator ai]
    (let [[patrol-area (patrol-area-locator ai.character.level)]
	  [target (.choice random patrol-area)]]
      (assoc ai.mode 1 target))))

(with-decorator log_debug
  (defn -patrol [is-patrol-area start-patrol ai action-factory]
    "routine to make character to patrol area"
    (let [[future-location (new-location ai.character (second ai.mode))]]
    (often (if (and (can-walk? ai action-factory (second ai.mode))
		    (is-patrol-area ai.character.level 
				    (first future-location)
				    (second future-location)))
	     (walk ai action-factory)
	     (if (is-patrol-area ai.character.level
				  (first ai.character.location)
				  (second ai.character.location))
	       (do (start-patrol ai)
		   (wait ai))
	       (walk-random-direction ai action-factory)))
    (wait ai)))))

(with-decorator log_debug
  (defn -walk-random-direction [ai action-factory]
    "take a random step without changing mode"
    (let [[legal-directions (list-comp direction 
				       [direction (range 1 9)] 
				       (.is-move-legal ai.character
						       direction
						       "walk"
						       action-factory))]]
      (if (len legal-directions) (assoc ai.mode 1
					(map-direction (.choice random 
								legal-directions)))
	  (assoc ai.mode 1 (map-direction (.randint random 1 8))))
      (if (can-walk? ai action-factory (second ai.mode)) (walk ai action-factory)
	  (wait ai)))))

(with-decorator log_debug
  (defn -find-patrol-area [is-patrollable start-patrolling patrol
			  move-towards-patrol-area select-patrol-area
			  ai action-factory]
    "routine to make character to find a patrol area"
    (if (is-patrollable ai.character.level
			(first ai.character.location)
			(second ai.character.location))
      (do (start-patrolling ai)
	  (patrol ai action-factory))
      (if (second ai.mode)
	(move-towards-patrol-area ai action-factory)
	(select-patrol-area ai)))))

(with-decorator log_debug
  (defn -patrollable-area-in-level [can-patrol level]
    "routine to find area to patrol in level"
    (let [[patrol-area []]]
      (foreach [x (range (len level.walls))]
	(foreach [y (range (len (first level.walls)))]
	  (if (can-patrol level x y)
	    (.append patrol-area (, x y)))))
      patrol-area)))

(defn -move-towards-patrol-area [ai action-factory]
  (let [[start-location ai.character.location]
	[path (first (a-star start-location
			     (second ai.mode)
			     ai.character.level))]]
    (if path
      (walk ai action-factory (find-direction start-location (second path)))
      (wait ai))))

(defn -get-random-patrol-direction [is-patrollable ai]
  "select a random direction to follow"
  (let [[possible-directions []]
	[character-x (first ai.character.location)]
	[character-y (second ai.character.location)]
	[level ai.character.level]]
    (for [x (range (- character-x 1) (+ character-x 2)) 
	  y (range (- character-y 1) (+ character-y 2))]
      (if (and (is-patrollable level x y)
	       (not (= (, x y) ai.character.location)))
	(.append possible-directions (, x y))))
    (if possible-directions 
      (find-direction ai.character.location (.choice random possible-directions)))))

(defn -enemy-close? [max-distance ai]
  "check if there is an enemy close by, returns preferred enemy"
  (let [[level ai.character.level]
	[player ai.character.model.player]]
    (if (< (distance-between player.location ai.character.location) max-distance)
      player)))

(defn -start-fighting [ai enemy]
  "start fighting against enemy"
  (focus-enemy ai enemy)
  (setv ai.mode [:fight
		 enemy]))

(defn -start-patrolling [get-random-patrol-direction ai]
  (setv ai.mode [:patrol
		 (get-random-patrol-direction ai)]))

(defn patrol-ai [is-patrol-area detection-distance]
  "factory function for creating patrolling ai"
  (let [[enemy-close? (partial -enemy-close? detection-distance)]
	[random-patrol-direction (partial -get-random-patrol-direction is-patrol-area)]
	[patrol-space (partial -patrollable-area-in-level is-patrol-area)]
	[select-area-to-patrol (partial -select-patrol-area patrol-space)]
	[close-in (partial -close-in-enemy 
		       (fn [start end level] (first (a-star start
							    end 
							    level))))]
	[fight (partial -fight-in-melee attack close-in)]
	[patrol (partial -patrol is-patrol-area (partial -start-patrolling random-patrol-direction))]
	[find-wall (partial -find-patrol-area is-patrol-area (partial -start-patrolling random-patrol-direction)
			patrol -move-towards-patrol-area
			select-area-to-patrol)]
	[act (fn [transit patrol fight ai model action-factory]
	  "main routine for patrol AI"
	  (if (not (= (first ai.mode) :fight))
	    (let [[enemy (enemy-close? ai)]]
	      (if enemy (-start-fighting ai enemy))))
	  (cond 
	   ((= (first ai.mode) :transit) (transit ai action-factory))
	   ((= (first ai.mode) :patrol) (patrol ai action-factory))
	   ((= (first ai.mode) :fight) (fight ai action-factory))))]]
    (partial act find-wall patrol fight)))
