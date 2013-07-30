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

(setv __doc__ "module for AI routines for rats")

(import [pyherc.aspects [logged]]
	[pyherc.ai.pathfinding [a-star]]
	[pyherc.ai.common [distance-between fight-in-melee find-direction]]
	[pyherc.ai.common [close-in-enemy walk can-walk? map-direction direction-mapping]]
	[pyherc.ai.common [patrol wait]]
	[pyherc.events [NoticeEvent]]
	[random]
	[math [sqrt]]
	[functools [partial]])

(require pyherc.ai.macros)

(defmacro diagonal-wall [info]
  (quasiquote (get (unquote info) 0)))

(defmacro adjacent-wall [info]
  (quasiquote (get (unquote info) 1)))

(defmacro empty-corridor [info]
  (quasiquote (get (unquote info) 2)))

(defmacro wall-direction [info]
  (quasiquote (get (unquote info) 3)))

(defclass RatAI []
  [[__doc__ "AI routine for rats"]
   [character None]
   [mode [:find-wall None]]
   [--init-- (fn [self character]
	       "default constructor"
	       (.--init-- (super RatAI self))
	       (setv self.character character) None)]
   [act (fn [self model action-factory rng] 
	  "check the situation and act accordingly"
	  (rat-act self model action-factory))]])

(with-decorator logged 
  (defn rat-act [ai model action-factory]
    "main routine for rat AI"
    (if (not (= (first ai.mode) :fight))
      (let [[enemy (enemy-close? ai)]]
	(if enemy (start-fighting ai enemy))))
    (let [[func (get mode-bindings (first ai.mode))]]
      (func ai action-factory))))

(defn is-next-to-wall? [level x y]
  "check if given location is within patrol area"
  (and (or (.blocks-movement level (+ x 1) y)
	   (.blocks-movement level (- x 1) y)
	   (.blocks-movement level x (+ y 1))
	   (.blocks-movement level x (- y 1)))
       (not (and (.blocks-movement level (+ x 1) y)
		 (.blocks-movement level (- x 1) y)))
       (not (and (.blocks-movement level x (+ y 1))
		 (.blocks-movement level x (- y 1))))))

(with-decorator logged
  (defn patrollable-area-in-level [ai]
    "routine to find area to patrol in level"
    (let [[level ai.character.level]
	  [patrol-area []]]
      (foreach [x (range (len level.walls))]
	(foreach [y (range (len (first level.walls)))]
	  (if (is-next-to-wall? level x y)
	    (.append patrol-area (, x y)))))
      patrol-area)))

(with-decorator logged
  (defn find-wall [ai action-factory]
    "routine to make character to find a wall"
    (if (is-next-to-wall? ai.character.level
			 (first ai.character.location)
			 (second ai.character.location))
      (do (start-following-wall ai)
	  (follow-wall ai action-factory))
      (if (second ai.mode)
	(move-towards-patrol-area ai action-factory)
	(select-patrol-area ai)))))

(defn move-towards-patrol-area [ai action-factory]
  (let [[start-location ai.character.location]
	[path (first (a-star start-location
			     (second ai.mode)
			     ai.character.level))]]
    (if path
      (walk ai action-factory (find-direction start-location (second path)))
      (wait ai))))

(defn select-patrol-area [ai]
  (let [[patrol-area (patrollable-area-in-level ai)]
	[target (.choice random patrol-area)]]
    (assoc ai.mode 1 target)))


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

(defn start-following-wall [ai]
  (setv ai.mode [:follow-wall 
		 (get-random-wall-direction ai)]))

(defn map-coordinates [location offset]
  "calculate new coordinates from character and offset"
  (let [[start-x (first location)]
	[start-y (second location)]
	[offset-x (first offset)]
	[offset-y (second offset)]]
    (, (+ start-x offset-x) (+ start-y offset-y))))

(defn get-random-wall-direction [ai]
  "select a random wall direction to follow"
  (let [[possible-directions []]
	[character-x (first ai.character.location)]
	[character-y (second ai.character.location)]
	[level ai.character.level]]
    (for [x (range (- character-x 1) (+ character-x 2)) 
	  y (range (- character-y 1) (+ character-y 2))]
      (if (and (is-next-to-wall? level x y)
	       (not (= (, x y) ai.character.location)))
	(.append possible-directions (, x y))))
    (if possible-directions 
      (find-direction ai.character.location (.choice random possible-directions))
      :north)))

(defn focus-enemy [ai enemy]
  "focus on enemy and start tracking it"
  (let [[character ai.character]
	[event (NoticeEvent character enemy)]]
    (.raise-event character event)))

(def close-in (partial close-in-enemy 
		       (fn [start end level] (first (a-star start
							    end 
							    level)))))
(def fight (partial fight-in-melee attack close-in))

(def follow-wall (partial patrol is-next-to-wall? start-following-wall))

(def mode-bindings {:find-wall find-wall
		    :follow-wall follow-wall
		    :fight fight})


