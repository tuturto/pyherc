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

(require hy.contrib.anaphoric)
(require pyherc.aspects)
(require pyherc.macros)
(import [pyherc.aspects [log-debug]]
	[pyherc.data.geometry [area-around]]
	[pyherc.events.mitosis [MitosisEvent]])

(defclass MitosisAction []
  [[--init-- #d(fn [self character character-generator rng]
		 "default constructor"
		 (-> (super) (.--init--))
		 (setv self.character character)
		 (setv self.character-generator character-generator)
		 (setv self.rng rng)
		 nil)]
   [legal? #d(fn [self]
	       "check if action is possible to perform"
	       (let [[location self.character.location]
		     [level self.character.level]
		     [tiles (area-around location)]]
		 (if
		     (list (ap-filter (not 
				       (or (.blocks-movement level (first it) (second it))
					   (.get-creature-at level it))) tiles))
		   true false)))]
   [execute #d(fn [self]
		"execute the action"
		(when (.legal? self)
		  (let [[new-character (self.character-generator self.character.name)]
			[location self.character.location]
			[level self.character.level]
			[tiles (list (genexpr tile [tile (area-around location)]))]]
		    (.add-creature level new-character (.choice self.rng tiles))
		    (.raise-event self.character (MitosisEvent self.character
							       new-character)))))]])

