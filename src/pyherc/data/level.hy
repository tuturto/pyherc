;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2015 Tuukka Turto
;; 
;; Permission is hereby granted, free of charge, to any person obtaining a copy
;; of this software and associated documentation files (the "Software"), to deal
;; in the Software without restriction, including without limitation the rights
;; to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
;; copies of the Software, and to permit persons to whom the Software is
;; furnished to do so, subject to the following conditions:
;; 
;; The above copyright notice and this permission notice shall be included in
;; all copies or substantial portions of the Software.
;; 
;; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
;; IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
;; FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
;; AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
;; LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
;; OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
;; THE SOFTWARE.

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
   :characters []
   :name nil
   :description nil})

(defn new-tile []
  "create a tile with default values"
  {:floor nil
   :wall nil
   :ornamentation []
   :traps []
   :tags []
   :items []
   :characters []
   :portal nil
   :features []})

(defn level-name [level &optional [name nil]]
  "get/set level name"
  (when name
    (assoc level :name name))
  (:name level))

(defn level-description [level &optional [description nil]]
  "get/set level description"
  (when description
    (assoc level :description description))
  (:description level))

(defn get-tile [level location]
  "get tile at given location"
  (when (in location (:tiles level))
    (get (:tiles level) location)))

(defn get-tiles [level]
  "get all tiles in level"
  (genexpr #t(location tile) [#t(location tile) (.items (:tiles level))]))

(defn tiles↜ [level]
  "get all tiles in level"
  (genexpr #t(location tile) [#t(location tile) (.items (:tiles level))]))

(defn get-or-create-tile [level location]
  "get tile at given location"
  (when (not (in location (:tiles level)))
    (assoc (:tiles level) location (new-tile)))
  (get (:tiles level) location))

(defn floor-tile [level location &optional [tile-id "no-tile"]]
  "get/set floor tile at given location"
  (if (!= tile-id "no-tile")
    (do (let [[map-tile (get-or-create-tile level location)]]
          (assoc map-tile :floor tile-id)
          (:floor map-tile)))
    (do (let [[map-tile (get-tile level location)]]
          (when map-tile (:floor map-tile))))))

(defn wall-tile [level location &optional [tile-id "no-tile"]]
  "get/set wall tile at given location"
  (assert (!= tile-id []))
  (if (!= tile-id "no-tile")
    (do (let [[map-tile (get-or-create-tile level location)]]
          (assoc map-tile :wall tile-id)
          (:wall map-tile)))
    (do (let [[map-tile (get-tile level location)]]
          (when map-tile (:wall map-tile))))))

(defn tile [level location]
  "get tile at given location, may be floor or wall"
  (let [[map-tile (get-tile level location)]]
    (when map-tile
      (when (:wall map-tile) (:wall map-tile))
      (when (:floor map-tile) (:floor map-tile)))))

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
                                 (safe-passage level (first pair)))]]
      (.choice random free-tiles)))

(defn blocks-movement [level location]
  "check if given location blocks movement"
  (let [[map-tile (get-tile level location)]]
    (if map-tile
      (if (:wall map-tile)
        true
        (if (:floor map-tile) false true))
      true)))

(defn free-passage [level location]
  "check if given location is free to move"
  (not (blocks-movement level location)))

(defn blocks-los [level location]
  "check if given location blocks line of sight"
  (wall-tile level location))

(defn safe-passage [level location]
  "check if given location is free to move without danger"
  (and (not (blocks-movement level location))
       (not (get-traps level location))
       (not (get-character level location))))

(defn ornamentation [level location &optional [tile-id "no-tile"]]
  (assert (!= tile-id []))
  (if (!= tile-id "no-tile")
    (do (let [[map-tile (get-or-create-tile level location)]]
          (.append (:ornamentation map-tile) tile-id)
          (:ornamentation map-tile)))
    (do (let [[map-tile (get-tile level location)]]
          (when map-tile (:ornamentation map-tile))))))

#d(defn add-item [level location item]
    "add item to level"
    (.append (:items level) item)
    (setv item.location location)
    (setv item.level level)
    (.append (:items (get-or-create-tile level location)) item)
    (ap-each (traps↜ level location) (.on-item-enter it item)))

(defn get-items [level &optional [location "no-location"]]
  "get items in a given tile or in level in general"
  (if (= location "no-location")
    (genexpr item [item (:items level)])
    (do
     (let [[map-tile (get-tile level location)]]
       (if (= map-tile nil)
         (genexpr item [item []])
         (genexpr item [item (:items map-tile)]))))))

#d(defn remove-item [level item]
    "removes item from level"
    (let [[map-tile (get-tile level item.location)]]
      (.remove (:items map-tile) item)
      (setv item.location #t())
      (setv item.level nil)
      (.remove (:items level) item)))

#d(defn add-character [level location character]
    "add character to level"
    (.append (:characters level) character)
    (setv character.location location)
    (setv character.level level)
    (.append (:characters (get-or-create-tile level location)) character))

(defn get-character [level location]
  #s("get characters in a given tile"
     "as a temporary measure, this will return only the first of characters."
     "TODO: replace/remove")  
  (let  [[map-tile (get-tile level location)]]
    (when map-tile
      (first (:characters map-tile)))))

(defn get-characters [level &optional [location nil]]
  "get all characters in level"
  (if location
    (let  [[map-tile (get-tile level location)]]
      (when map-tile
        (:characters map-tile)))
    (genexpr character [character (:characters level)])))

#d(defn remove-character [level character]
    "remove character from level"
    (when character.location
      (.remove (:characters (get-tile level character.location)) character))
    (setv character.location #t())
    (when (in character (:characters level))
      (.remove (:characters level) character)))

#d(defn move-character [level location character]
    "move character to a new location"
    (remove-character character.level character)
    (add-character level location character))

#d(defn add-trap [level location trap]
    "add trap to level"
    (.append (:traps (get-or-create-tile level location)) trap)    
    (setv trap.level level)
    (setv trap.location location)
    (.on-place trap level location))

(defn remove-trap [level trap]
  "remove trap from level"
  (.remove (:traps (get-tile level trap.location)) trap))

(defn traps↜ [level location]
  "get traps in a given location"
  (let  [[map-tile (get-tile level location)]]
    (if map-tile 
      (genexpr x [x (:traps map-tile)])
      (genexpr x [x []]))))

(defn get-traps [level location]
  "get traps at given location"
  (let [[map-tile (get-tile level location)]]
    (if map-tile
      (:traps map-tile)
      [])))

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

(defn location-features [level location]
  "get features in a given location"
  (let [[map-tile (get-tile level location)]]
    (if map-tile
      (genexpr feature [feature (:features map-tile)])
      (genexpr feature [feature []]))))

(defn add-location-feature [level location feature]
  "add location feature"
  (let [[map-tile (get-tile level location)]]
    (.append (:features map-tile) feature)))

(defn remove-location-feature [level location feature]
  "remove a location feature"
  (let [[map-tile (get-tile level location)]]
    (.remove (:features map-tile) feature)))
