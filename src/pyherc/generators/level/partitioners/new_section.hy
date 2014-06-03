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

(require pyherc.macros)

(import [pyherc.data [add-location-tag add-trap floor-tile wall-tile
                      ornamentation]])

(defn new-section [corner0 corner1 level]
  "create a new section"
  {:corners [corner0 corner1]
   :level level
   :connections []
   :room-connections []
   :neighbours []})

(defn section-corners [section &optional [corners :no-corners]]
  "get/set corners of this section"
  (when (!= corners :no-corners) (setv section._corners corners))
  section._corners)

(defn section-height [section]
  "get height of a section"
  (abs (- (y-coordinate (first section.-corners))
          (y-coordinate (second section.-corners)))))

(defn section-width [section]
  "get width of a section"
  (abs (- (x-coordinate (first section.-corners))
          (x-coordinate (second section.-corners)))))

(defn left-edge [section]
  "get left edge of the section"
  (let [[point₀ (x-coordinate (first section.-corners))]
        [point₁ (x-coordinate (second section.-corners))]]
    (if (< point₀ point₁) point₀ point₁)))

(defn right-edge [section]
  "get right edge of the section"
  (let [[point₀ (x-coordinate (first section.-corners))]
        [point₁ (x-coordinate (second section.-corners))]]
    (if (> point₀ point₁) point₀ point₁)))

(defn top-edge [section]
  "get top edge of the section"
  (let [[point₀ (y-coordinate (first section.-corners))]
        [point₁ (y-coordinate (second section.-corners))]]
    (if (< point₀ point₁) point₀ point₁)))

(defn bottom-edge [section]
  "get bottom edge of the section"
  (let [[point₀ (y-coordinate (first section.-corners))]
        [point₁ (y-coordinate (second section.-corners))]]
    (if (> point₀ point₁) point₀ point₁)))

(defn section-to-map [section location]
  "map section coordinates to map coordinates"
  #t((+ (left-edge section) (x-coordinate location))
     (+ (top-edge section) (y-coordinate location))))

(defn section-floor [section location &optional [tile-id :no-tile] location-type]
  "get/set floor tile in section"
  (let [[loc (section-to-map section location)]
        [level section.level]]
    (when (!= tile-id :no-tile) (floor-tile level loc tile-id))
    (when location-type (add-location-tag level loc location-type))
    (floor-tile level loc tile-id)))

(defn section-wall [section location &optional [tile-id :no-tile] location-type]
  "get/set wall tile in section"
  (let [[loc (section-to-map section location)]
        [level section.level]]
    (when (!= tile-id :no-tile) (wall-tile level loc tile-id))
    (when location-type (add-location-tag level loc location-type))
    (wall-tile level loc tile-id)))

(defn section-ornamentation [section location &optional [tile-id :no-tile]]
  "get/set ornament in section"
  (let [[loc (section-to-map section location)]
        [level section.level]]
    (when (!= tile-id :no-tile) (ornamentation level loc tile-id))
    (ornamentation level loc tile-id)))

(defn section-trap [section location trap]
  "set trap in section"
  (add-trap section.level (section-to-map section location) trap))
