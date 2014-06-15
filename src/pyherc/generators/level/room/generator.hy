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
(require pyherc.macros)

(import [pyherc.data [distance-between]]
        [pyherc.generators.level.partitioners [section-floor
                                               section-floor
                                               section-data]]
        [pyherc.generators.level.room.corridor [corridors]]
        [pyherc.generators.level.room.shapes [circular-shape]])

(defn new-room-generator [&rest creators]
  "create a room generator"
  (fn [section]
    (ap-each creators (it section))))

(defn cache-creator [cache-tile item-selector character-selector]
  "create cache creator"
  (fn [section]
    "fill cache with items and characters"
    (section-floor section (section-data section :center-point) cache-tile)))

(defn tomes-and-potions-cache [item-generator]
  "create cache content creator"
  (fn []
    []))

(defn no-characters-cache [character-generator]
  "create cache character creator"
  (fn []
    []))

(defn demo [floor-tile corridor-tile cache-tile item-generator character-generator] 
  (new-room-generator (circular-shape floor-tile)
                      (corridors corridor-tile)
                      (cache-creator cache-tile
                                     (tomes-and-potions-cache item-generator)
                                     (no-characters-cache character-generator))))

