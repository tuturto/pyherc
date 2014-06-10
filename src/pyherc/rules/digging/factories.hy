;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2014 Tuukka Turto
;;
;;  This file is part of pyherc.
;;
;;  pyherc is free software: you can redistribute it and/or modify
;;  it under the terms of the GNU General Public License as published by
;;  the Free Software Foundation, either version 3 of the License, or
;;  (at your option) any later version.
;;
;;  pyherc is distributed in the hope that it will be useful,
;;  but WITHOUT ANY WARRANTY; without even the implied warranty of
;;  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;  GNU General Public License for more details.
;;
;;  You should have received a copy of the GNU General Public License
;;  along with pyherc.  If not, see <http://www.gnu.org/licenses/>.


(require hy.contrib.anaphoric)
(require pyherc.aspects)
(require pyherc.macros)

(import [pyherc.aspects [log-debug log-info]]
        [pyherc.data [location-features]]
        [pyherc.data.features [feature-type]]
	[pyherc.rules.exhuming.action [DigAction]])

(defclass DigFactory []
  [[--init-- #i(fn [self rng]
		 "default constructor"
		 (-> (super) (.--init--))
		 (setv self.action-type "dig")
                 (setv self.rng rng)
		 nil)]
   [can-handle #d(fn [self parameters]
		   "can this factory handle a given action"
		   (= self.action-type parameters.action-type))]
   [get-action #d(fn [self parameters]
		   "create digging action"
                   (let [[character parameters.character]
                         [location character.location]
                         [level character.level]
                         [cache (get-cache level location)]]
                     (DigAction character cache self.rng)))]])

(defn get-cache [level location]
  (let [[caches (list-comp feature 
                           [feature (location-features level location)]
                           (= (feature-type feature) :cache))]]
    (when (> (count caches) 0)
      (first (list caches)))))
