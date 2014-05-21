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

(import [pyherc.aspects [log_debug]])
(require pyherc.aspects)
(require pyherc.macros)

(defn new-tile []
  "create a tile with default values"
  {:floor nil
   :wall nil
   :ornamentations []
   :trap nil
   :location_types []
   :items []
   :creatures []
   :portal nil})

(defn get-tile [level location]
  "get tile at given location"
  (when (not (in location level.tiles))
    (assoc level.tiles location (new-tile)))
  (get level.tiles location))

(defn floor-tile [level location &optional tile-id]
  "get/set floor tile at given location"
  (when tile-id
     (assoc (get-tile level location) :floor tile-id))
  (:floor (get-tile level location)))

#d(defn add-portal [level location portal &optional other-end]
    "add a new portal"
    (setv portal.level level)
    (setv portal.location location)
    (floor-tile level location portal.icon)
    (assoc (get-tile level location) :portal portal)
    (when other-end
      (.set-other-end portal other-end)
      (.set-other-end other-end portal)))
