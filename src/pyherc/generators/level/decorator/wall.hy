;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2015 Tuukka Turto
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

(import [pyherc.generators.level.decorator.basic [Decorator DecoratorConfig]]
        [pyherc.aspects [log-debug log-info]]
        [pyherc.data [wall-tile floor-tile get-tiles area-around
                      ornamentation get-locations-by-tag add-location-tag]]
        [pyherc.data.geometry [area-around]]
        [pyherc.data.level [tiles↜]]
        [random])
(require pyherc.macros)
(require pyherc.aspects)
(require hy.contrib.anaphoric)

(defclass SurroundingDecorator [Decorator]
  [[--init-- #d(fn [self configuration]
                 "default constructor"
                 (-> (super) (.--init-- configuration))
                 (setv self.wall-tile configuration.wall-tile)
                 nil)]
   [decorate-level #i(fn [self level]
                       "decorate a level"
                       (ap-each (list (get-tiles level))
                                (decorate-tile level it self.wall-tile)))]])

(defn decorate-tile [level loc-tile replacement]
  "decorate single tile"
  (let [[#t(location tile) loc-tile]
        [surrounding-tiles (area-around location)]]
    (ap-each (ap-filter (and (= (wall-tile level it) null)
                             (= (floor-tile level it) null))
                        surrounding-tiles)
             (wall-tile level it replacement))))

(defclass SurroundingDecoratorConfig [DecoratorConfig]
  [[--init-- #d(fn [self level-types wall-tile]
                 "default constructor"
                 (-> (super) (.--init-- level-types))
                 (setv self.wall-tile wall-tile)
                 nil)]])

(defn wall-ornamenter [left-wall top-wall right-wall rate rng]
  "create decorator to ornament walls"
  (fn [level]
    "decorate level"
    (ap-each (list (get-tiles level))
             (add-ornament level it left-wall top-wall right-wall rate rng))))

(defn add-ornament [level loc-tile left-wall top-wall right-wall rate rng]
  (let [[#t(location tile) loc-tile]
        [#t(x-loc y-loc) location]]
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

(defn floor-swap [source target rate rng]
  "decorator used to replace one floor tile to another"
  (fn [level]
    (ap-each (list (get-tiles level))
             (swap-floor-tile level it source target rate rng))))

(defn swap-floor-tile [level loc-tile source target rate rng]
  (let [[#t(location tile) loc-tile]]
    (when (and (= (floor-tile level location) source)
               (<= (.randint rng 0 100) rate))
      (floor-tile level location target))))

(defn wall-swap [tiles tag tile-dict]
  "decorator used to replace set of wall tiles with another set"
  (fn [level]
    (ap-each (tiles level tag) 
             (let [[old-tile (wall-tile level it)]]
               (when (in old-tile tile-dict)
                 (wall-tile level it (get tile-dict old-tile)))))))

(defn floor-swap-2 [tiles tile-dict]
  "decorator used to replace set of floor tiles with another set"
  (fn [level]
    (ap-each (tiles level) (when (in (:floor (second it)) tile-dict)
                             (assoc (second it) :floor 
                                    (get tile-dict (:floor (second it))))))))

(defn coarse-selection [level tag]
  "tag some of the tiles in level and return them"
  (let [[location-value (dict-comp (first x) (.uniform random -1.0 1.0)
                                   [x (tiles↜ level)])]
        [get-value (fn [point data]
                     (if (in point data)
                       (get data point)
                       0))]
        [coarsify-point (fn [point data]
                          (let [[area↜ (area-around point)]
                                [value-sum (sum (list-comp (get-value x data) [x area↜]))]
                                [score (+ (get-value point data)
                                          (* value-sum 0.05))]]))]
        [coarsify (fn [data]
                    (dict-comp (first x) (coarsify-point (first x) data) [x (.items data)]))]]
    (when (not (list (get-locations-by-tag level tag)))
      (for [i (range 50)] 
        (setv location-value (coarsify location-value)))
      (ap-each (tiles↜ level)
               (when (> (get location-value (first it)) 0.0)
                 (add-location-tag level (first it) tag))))        
    (get-locations-by-tag level tag)))
