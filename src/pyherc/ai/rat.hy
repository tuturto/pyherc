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
	[pyherc.ai.common [patrol close-in-enemy fight-in-melee]]
	[pyherc.ai.common [patrollable-area-in-level select-patrol-area]]
	[pyherc.ai.common [move-towards-patrol-area get-random-patrol-direction]]
	[pyherc.ai.common [find-patrol-area enemy-close?]]
	[pyherc.ai.basic [can-walk? walk wait distance-between find-direction]]
	[pyherc.ai.basic [map-direction direction-mapping attack focus-enemy]]
	[random]
	[math [sqrt]]
	[functools [partial]])

(require pyherc.ai.macros)

(defclass RatAI []
  [[__doc__ "AI routine for rats"]
   [character None]
   [mode [:transit None]]
   [--init-- (fn [self character]
	       "default constructor"
	       (.--init-- (super RatAI self))
	       (setv self.character character) None)]
   [act (fn [self model action-factory rng] 
	  "check the situation and act accordingly"
	  (rat-act self model action-factory))]])

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

(defn start-fighting [ai enemy]
  "start fighting against enemy"
  (focus-enemy ai enemy)
  (setv ai.mode [:fight
		 enemy]))

(defn start-following-wall [get-random-wall-direction ai]
  (setv ai.mode [:patrol
		 (get-random-wall-direction ai)]))

(defn patrol-ai [is-patrol-area detection-distance]
  (let [[is-enemy-close? (partial enemy-close? 4)]
	[get-random-wall-direction (partial get-random-patrol-direction is-next-to-wall?)]
	[wall-space (partial patrollable-area-in-level is-next-to-wall?)]
	[select-wall-to-patrol (partial select-patrol-area wall-space)]
	[close-in (partial close-in-enemy 
		       (fn [start end level] (first (a-star start
							    end 
							    level))))]
	[fight (partial fight-in-melee attack close-in)]
	[follow-wall (partial patrol is-next-to-wall? (partial start-following-wall get-random-wall-direction))]
	[find-wall (partial find-patrol-area is-next-to-wall? (partial start-following-wall get-random-wall-direction)
			follow-wall move-towards-patrol-area
			select-wall-to-patrol)]
	[act (fn [transit patrol fight ai model action-factory]
	  "main routine for rat AI"
	  (if (not (= (first ai.mode) :fight))
	    (let [[enemy (is-enemy-close? ai)]]
	      (if enemy (start-fighting ai enemy))))
	  (cond 
	   ((= (first ai.mode) :transit) (transit ai action-factory))
	   ((= (first ai.mode) :patrol) (patrol ai action-factory))
	   ((= (first ai.mode) :fight) (fight ai action-factory))))]]
    (partial act find-wall follow-wall fight)))

(def rat-act (patrol-ai is-next-to-wall? 4))
