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

(import [pyherc.aspects [log_debug]]
        [functools [reduce]]
        [random])
(require hy.contrib.anaphoric)
(require pyherc.aspects)
(require pyherc.macros)

(defn new-level [model]
  "create a new level"
  {:model model
   :tiles {}
   :items []
   :characters []})

(defn new-tile []
  "create a tile with default values"
  {:floor nil
   :wall nil
   :ornamentation nil
   :trap nil
   :tags []
   :items []
   :character nil
   :portal nil})

(defn get-tile [level location]
  "get tile at given location"
  (when (in location (:tiles level))
    (get (:tiles level) location)))

(defn get-tiles [level]
  "get all tiles in level"
  (genexpr #t(location tile) [#t(location tile) (.items (:tiles level))]))

(defn get-or-create-tile [level location]
  "get tile at given location"
  (when (not (in location (:tiles level)))
    (assoc (:tiles level) location (new-tile)))
  (get (:tiles level) location))

(defn floor-tile [level location &optional [tile-id :no-tile]]
  "get/set floor tile at given location"
  (if (!= tile-id :no-tile)
    (do (let [[map-tile (get-or-create-tile level location)]]
          (assoc map-tile :floor tile-id)
          (:floor map-tile)))
    (do (let [[map-tile (get-tile level location)]]
          (when map-tile (:floor map-tile))))))

(defn wall-tile [level location &optional [tile-id :no-tile]]
  "get/set wall tile at given location"
  (if (!= tile-id :no-tile)
    (do (let [[map-tile (get-or-create-tile level location)]]
          (assoc map-tile :wall tile-id)
          (:wall map-tile)))
    (do (let [[map-tile (get-tile level location)]]
          (when map-tile (:wall map-tile))))))

(defn tile [level location]
  "get tile at given location, may be floor or wall"
  (let [[map-tile (get-tile level location)]]
    (when map-tile
      (when :wall map-tile (:wall map-tile))
      (when :floor map-tile (:floor map-tile)))))

#d(defn add-portal [level location portal &optional other-end]
    "add a new portal"
    (setv portal.level level)
    (setv portal.location location)
    (floor-tile level location portal.icon)
    (assoc (get-tile level location) :portal portal)
    (when other-end
      (.set-other-end portal other-end)
      (.set-other-end other-end portal)))

#d(defn get-portal [level location]
    "get portal at given location"
    (:portal (get-tile level location)))

(defn level-size [level]
  "get size of level (x₀, x₁, y₀, y₁)"
  (let [[x₀ 0] [x₁ 0] [y₀ 0] [y₁ 0]]
    (ap-each (:tiles level)
             (do
              (when (< (first it) x₀) (setv x₀ (first it)))
              (when (> (first it) x₁) (setv x₁ (first it)))
              (when (< (second it) y₀) (setv y₀ (second it)))
              (when (> (second it) y₁) (setv y₁ (second it)))))
    #t(x₀ x₁ y₀ y₁)))

#d(defn find-free-space [level]
    "find a free location within level"
    (let [[free-tiles (list-comp (first pair)
                                 [pair (.items (:tiles level))] 
                                 (and (= (:wall (second pair)) nil)
                                      (:floor (second pair))))]]
      (.choice random free-tiles)))

(defn blocks-movement [level location]
  "check if given location blocks movement"
  (let [[map-tile (get-tile level location)]]
    (if map-tile
      (:wall map-tile)
      true)))

(defn blocks-los [level location]
  "check if given location blocks line of sight"
  (wall-tile level location))

(defn ornamentation [level location &optional [tile-id :no-tile]]
  (if (!= tile-id :no-tile)
    (do (let [[map-tile (get-or-create-tile level location)]]
          (assoc map-tile :ornamentation tile-id)
          (:ornamentation map-tile)))
    (do (let [[map-tile (get-tile level location)]]
          (when map-tile (:ornamentation map-tile))))))

#d(defn add-item [level location item]
    "add item to level"
    (.append (:items level) item)
    (setv item.location location)
    (setv item.level level)
    (.append (:items (get-or-create-tile level location)) item))

(defn get-items [level &optional [location :no-location]]
  "get items in a given tile or in level in general"
  (if (= location :no-location)
    (list-comp item [item (:items level)])
    (do
     (let [[map-tile (get-tile level location)]]
       (if (= map-tile nil)
         []
         (list-comp item [item (:items map-tile)]))))))

#d(defn remove-item [level item]
    "removes item from level"
    (let [[map-tile (get-tile level item.location)]]
      (.remove (:items map-tile) item)
      (setv item.location #t())
      (.remove (:items level) item)))

#d(defn add-character [level location character]
    "add character to level"
    (.append (:characters level) character)
    (setv character.location location)
    (setv character.level level)
    (assoc (get-or-create-tile level location) :character character))

(defn get-character [level location]
  "get characters in a given tile"
  (let  [[map-tile (get-tile level location)]]
    (when map-tile
      (:character map-tile))))

(defn get-characters [level]
  "get all characters in level"
  (genexpr character [character (:characters level)]))

#d(defn remove-character [level character]
    "remove character from level"
    (assoc (get-tile level character.location) :character nil)
    (setv character.location #t())
    (.remove (:characters level) character))

#d(defn move-character [level location character]
    "move character to a new location"
    (remove-character character.level character)
    (add-character level location character))

#d(defn add-trap [level location trap]
    "add trap to level"
    (assoc (get-or-create-tile level location) :trap trap))

(defn get-trap [level location]
  "get trap in a given tile"
  (let  [[map-tile (get-tile level location)]]
    (when map-tile
      (:trap map-tile))))

(defn add-location-tag [level location tag]
  "add tag to given location"
  (let [[map-tile (get-or-create-tile level location)]]
    (.append (:tags map-tile) tag)))

(defn get-location-tags [level location]
  "get tags in given location"
  (let [[map-tile (get-tile level location)]]
    (if map-tile
      (genexpr tag [tag (:tags map-tile)])
      (genexpr tag [tag []]))))

(defn get-locations-by-tag [level tag]
  "get locations by tag"
  (genexpr location [#t(location tile) (.items (:tiles level))] 
           (or (in tag (:tags tile))
               (= tag "any"))))
