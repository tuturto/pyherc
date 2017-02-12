;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2017 Tuukka Turto
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

(import [pyherc.generators.level.decorator.basic [Decorator DecoratorConfig]]
        [pyherc.aspects [log-debug log-info]]
        [pyherc.data [wall-tile floor-tile get-tiles area-around
                      ornamentation get-locations-by-tag add-location-tag]]
        [pyherc.data.geometry [area-around]]
        [pyherc.data.level [tiles↜]]
        [random])
(require [pyherc.macros [*]])
(require [pyherc.aspects [*]])
(require [hy.extra.anaphoric [ap-each ap-filter]])

(defclass SurroundingDecorator [Decorator]

  (defn --init-- [self configuration]
    "default constructor"
    (-> (super) (.--init-- configuration))
    (setv self.wall-tile configuration.wall-tile))
  
  (defn decorate-level [self level]
    "decorate a level"
    (ap-each (list (get-tiles level))
             (decorate-tile level it self.wall-tile))))

(defn decorate-tile [level loc-tile replacement]
  "decorate single tile"
  (let [#t(location tile) loc-tile
        surrounding-tiles (area-around location)]
    (ap-each (ap-filter (and (= (wall-tile level it) None)
                             (= (floor-tile level it) None))
                        surrounding-tiles)
             (wall-tile level it replacement))))

(defclass SurroundingDecoratorConfig [DecoratorConfig]
  
  (defn --init-- [self level-types wall-tile]
    "default constructor"
    (-> (super) (.--init-- level-types))
    (setv self.wall-tile wall-tile)))

(defn wall-ornamenter [left-wall top-wall right-wall rate rng]
  "create decorator to ornament walls"
  (fn [level]
    "decorate level"
    (ap-each (list (get-tiles level))
             (add-ornament level it left-wall top-wall right-wall rate rng))))

(defn add-ornament [level loc-tile left-wall top-wall right-wall rate rng]
  (let [#t(location tile) loc-tile
        #t(x-loc y-loc) location]
    (when (and left-wall
               (floor-tile level #t((inc x-loc) y-loc))
               (= (wall-tile level location) (first left-wall))
               (<= (.randint rng 0 100) rate))
      (ornamentation level location (.choice rng (second left-wall))))
    (when (and right-wall
               (floor-tile level #t((dec x-loc) y-loc))
               (= (wall-tile level location) (first right-wall))
               (<= (.randint rng 0 100) rate))
      (ornamentation level location (.choice rng (second right-wall))))
    (when (and top-wall
               (floor-tile level #t(x-loc (inc y-loc)))
               (= (wall-tile level location) (first top-wall))
               (<= (.randint rng 0 100) rate))
      (ornamentation level location (.choice rng (second top-wall))))))

(defn wall-swap [tiles tag tile-dict]
  "decorator used to replace set of wall tiles with another set"
  (fn [level]
    (ap-each (tiles level tag) 
             (let [old-tile (wall-tile level it)]
               (when (in old-tile tile-dict)
                 (wall-tile level it (get tile-dict old-tile)))))))

(defn floor-swap [tiles tag tile-dict]
  "decorator used to replace set of floor tiles with another set"
  (fn [level]
    (ap-each (tiles level tag) 
             (let [old-tile (floor-tile level it)]
               (when (in old-tile tile-dict)
                 (floor-tile level it (get tile-dict old-tile)))))))

(defn random-selection [rng rate level tag]
  "tag some of the tiles in level and return them"
  (when (not (list (get-locations-by-tag level tag)))
    (ap-each (tiles↜ level)
             (when (<= (.randint rng 0 100) rate)
               (add-location-tag level (first it) tag))))
  (get-locations-by-tag level tag))

(defn coarse-selection [level tag]
  "tag some of the tiles in level and return them"
  (def location-value (dict-comp (first x) (.uniform random -1.0 1.0)
                                 [x (tiles↜ level)]))

  (defn get-value [point data]
    (if (in point data)
      (get data point)
      0))

  (defn coarsify-point [point data]
    (let [area↜ (area-around point)
          value-sum (sum (list-comp (get-value x data) [x area↜]))
          score (+ (get-value point data)
                   (* value-sum 0.025))]
      score))

  (defn coarsify [data]
    (dict-comp x (coarsify-point x data) [x (.keys data)]))
  
  (when (not (list (get-locations-by-tag level tag)))
    (for [i (range 25)] 
      (setv location-value (coarsify location-value)))
    (ap-each (tiles↜ level)
             (when (> (get location-value (first it)) 0.0)
               (add-location-tag level (first it) tag))))        
  (get-locations-by-tag level tag))
