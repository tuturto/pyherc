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

(import [pyherc.aspects [logged]])

(defclass RatAI []
  [[__doc__ "AI routine for rats"]
   [character None]
   [mode [:find-wall :north]]
   [--init-- (fn [self character]
	       "default constructor"
	       (.--init-- (super RatAI self))
	       (setv self.character character) None)]
   [act (fn [self model action-factory rng] 
	  "check the situation and act accordingly"
	  (rat-act self model action-factory rng))]])

(with-decorator logged 
  (defn rat-act [ai model action-factory rng]
    "main routine for rat AI"
    (let [[func (get mode-bindings (get ai.mode 0))]]
      (func ai model action-factory rng))))

(defn find-wall [ai model action-factory rng]
  "routine to make character to find a wall"
    (let [[character ai.character]
	  [wall-info (next-to-wall? character)]]
      (if wall-info (setv ai.mode [:follow-wall (get-random-wall-direction wall-info rng)])
	  (if (.is-move-legal character (map-direction (get ai.mode 1)) "walk" action-factory)
	    (.move character (map-direction (get ai.mode 1)) action-factory)
	    (do (assoc ai.mode 1 (map-direction (.randint rng 1 8)))
		(setv ai.character.tick 5))))))

(defn follow-wall [ai model action-factory rng]
  "routine to make character to follow a wall"
  (let [[character ai.character]]
    (if (.is-move-legal character (map-direction (get ai.mode 1)) "walk" action-factory)
      (.move character (map-direction (get ai.mode 1)) action-factory)
      (let [[wall-info (next-to-wall? character)]]
	(if wall-info (do (setv ai.mode [:follow-wall (get-random-wall-direction wall-info rng)])
			  (setv ai.character.tick 5))
	   (setv ai.character.tick 50))))))

;; wall-mapping
;; first two elements are offsets for required walls
;; third element is offset for required empty space
;; fourth element is resulting direction
(def wall-mapping [[[-1 1]  [0 1]  [-1 0] :west]
		   [[-1 -1] [0 -1] [-1 0] :west]
		   [[1 1]   [0 1]  [1 0]  :east]
		   [[1 -1]  [0 -1] [1 0]  :east]
		   [[-1 1]  [-1 0] [0 1]  :south]
		   [[1 1]   [1 0]  [0 1]  :south]
		   [[-1 -1] [-1 0] [0 -1] :north]
		   [[1 -1]  [1 0]  [0 -1] :north]])

(defn next-to-wall? [character]
  "check if character is standing next to a wall"
  (let [[possible-directions (list-comp (check-wall-mapping character x) [x wall-mapping])]
	[directions (list-comp direction [direction possible-directions] (not (= direction None)))]]
    (if (> (len directions) 0) {:wall-direction directions} None)))

(defn check-wall-mapping [character wall-mapping]
  "build a list of directions where a wall leads from given location"
  (let [[level character.level]
	[point-1 (map-coordinates character (get wall-mapping 0))]
	[point-2 (map-coordinates character (get wall-mapping 1))]
	[point-3 (map-coordinates character (get wall-mapping 2))]]
    (if (and (.blocks-movement level (get point-1 0) (get point-1 1))
             (.blocks-movement level (get point-2 0) (get point-2 1))
	     (not (.blocks-movement level (get point-3 0) (get point-3 1))))
	  (get wall-mapping 3))))

(defn map-coordinates [character offset]
  "calculate new coordinates from character and offset"
  (let [[character-x (get character.location 0)]
	[character-y (get character.location 1)]
	[offset-x (get offset 0)]
	[offset-y (get offset 1)]]
    (, (+ character-x offset-x) (+ character-y offset-y))))

(defn get-random-wall-direction [wall-info rng]
  "select a random direction from the given wall-info"
  (.choice rng (:wall-direction wall-info)))

(def mode-bindings {:find-wall find-wall
		    :follow-wall follow-wall})

(def direction-mapping {1 :north 2 :north-east 3 :east 4 :south-east 5 :south
			6 :south-west 7 :west 8 :north-west 9 :enter
			:north 1 :north-east 2 :east 3 :south-east 4 :south 5
			:south-west 6 :west 7 :north-west 8 :enter 9})

(defn map-direction [direction]
  "map between keyword and integer directions"
  (get direction-mapping direction))
