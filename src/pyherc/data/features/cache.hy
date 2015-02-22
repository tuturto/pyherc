;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2015 Tuukka Turto
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

(defn new-cache [level location items characters]
  "create a new cache"
  {:type :cache
   :location location
   :level level
   :items items
   :characters characters})

(defn feature-type [feature]
  "type of the special feature"
  (:type feature))

(defn feature-location [entity &optional [location :no-location]]
  "get/set location of an entity"
  (when (!= location :no-location) (assoc entity :location location))
  (:location entity))

(defn feature-level [entity &optional [level :no-level]]
  "get/set level of an entity"
  (when (!= level :no-level) (assoc entity :level level))
  (:level entity))

(defn items-in-cache [cache]
  "get items in cache"
  (genexpr item [item (:items cache)]))

(defn characters-in-cache [cache]
  "get characters in cache"
  (genexpr character [character (:characters cache)]))

(defn clear-cache [cache]
  "empties this cache completely"
  (assoc cache :items [])
  (assoc cache :characters []))
