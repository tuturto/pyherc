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
	[pyherc.ai.common [patrol-ai]])

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

(def rat-act (patrol-ai is-next-to-wall? 4))
