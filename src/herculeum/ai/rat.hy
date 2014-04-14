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

(setv __doc__ "module for AI routines for rats")

(import [herculeum.ai.patrol [patrol-ai]])

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

(defn next-to-wall? [level x y]
  "check if given location is within patrol area"
  (and (or (.blocks-movement level (inc x) y)
	   (.blocks-movement level (dec x) y)
	   (.blocks-movement level x (inc y))
	   (.blocks-movement level x (dec y)))
       (not (and (.blocks-movement level (inc x) y)
		 (.blocks-movement level (dec x) y)))
       (not (and (.blocks-movement level x (inc y))
		 (.blocks-movement level x (dec y))))
       (.get-floor-tile level x y)))

(def rat-act (patrol-ai next-to-wall? 4))
