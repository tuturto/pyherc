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
	[pyherc.rules.exhuming.action [ExhumeAction]])

(defclass ExhumeFactory []
  [[--init-- #i(fn [self]
		 "default constructor"
		 (-> (super) (.--init--))
		 (setv self.action-type "exhume")
		 nil)]
   [can-handle #d(fn [self parameters]
		   "can this factory handle a given action"
		   (= self.action-type parameters.action-type))]
   [get-action #d(fn [self parameters]
		   "create exhuming action"
                   (let [[character parameters.character]
                         [location character.location]
                         [level character.level]
                         [grave (get-grave level location)]]
                     (ExhumeAction character grave)))]])

(defn get-grave [level location]
  (let [[graves (list-comp feature 
                         [feature (location-features level location)]
                         (= (feature-type feature) :grave))]]
    (when (> (count graves) 0)
      (first (list graves)))))