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
	[pyherc.ai.helpers [map-direction]])

(require pyherc.ai.helpers)

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
    (let [[func (get mode-bindings (first ai.mode))]]
      (func ai model action-factory rng))))

(defn find-wall [ai model action-factory rng]
  "routine to make character to find a wall"
  (let [[character ai.character]
	[wall-info (next-to-wall? character)]]
    (if wall-info (setv ai.mode [:follow-wall (get-random-wall-direction wall-info rng)])
	(if (.is-move-legal character (map-direction (second ai.mode)) "walk" action-factory)
	  (.move character (map-direction (second ai.mode)) action-factory)
	  (do (assoc ai.mode 1 (map-direction (.randint rng 1 8)))
	      (if (.is-move-legal character (map-direction (second ai.mode)) "walk" action-factory)
		(.move character (map-direction (second ai.mode)) action-factory)
		(setv ai.character.tick 5)))))))

(defn follow-wall [ai model action-factory rng]
  "routine to make character to follow a wall"
  (let [[character ai.character]]
    (if (.is-move-legal character (map-direction (second ai.mode)) "walk" action-factory)
      (.move character (map-direction (second ai.mode)) action-factory)
      (let [[wall-info (next-to-wall? character)]]
	(if wall-info (do (setv ai.mode [:follow-wall (get-random-wall-direction wall-info rng)])
			  (setv ai.character.tick 5))
	    (do (assoc ai.mode 1 (map-direction (.randint rng 1 8)))
		(if (.is-move-legal character (map-direction (second ai.mode)) "walk" action-factory)
		  (.move character (map-direction (second ai.mode)) action-factory)
		  (setv ai.character.tick 5))))))))

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
	[point-1 (map-coordinates character (diagonal-wall wall-mapping))]
	[point-2 (map-coordinates character (adjacent-wall wall-mapping))]
	[point-3 (map-coordinates character (empty-corridor wall-mapping))]]
    (if (and (.blocks-movement level (first point-1) (second point-1))
             (.blocks-movement level (first point-2) (second point-2))
	     (not (.blocks-movement level (first point-3) (second point-3))))
	  (wall-direction wall-mapping))))

(defn map-coordinates [character offset]
  "calculate new coordinates from character and offset"
  (let [[character-x (first character.location)]
	[character-y (second character.location)]
	[offset-x (first offset)]
	[offset-y (second offset)]]
    (, (+ character-x offset-x) (+ character-y offset-y))))

(defn get-random-wall-direction [wall-info rng]
  "select a random direction from the given wall-info"
  (.choice rng (:wall-direction wall-info)))

(def mode-bindings {:find-wall find-wall
		    :follow-wall follow-wall})


