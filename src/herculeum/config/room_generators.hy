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

(import [pyherc.data.traps [PitTrap]]
        [pyherc.generators.level.room [new-room-generator square-shape
                                       circular-shape corridors
                                       add-rows cache-creator mark-center-area
                                       random-rows trap-creator
                                       wall-creator
                                       center-area]])

(defn square-room [floor-tile corridor-tile rng]
  "create room generator for square rooms"
  (new-room-generator (square-shape floor-tile rng)
                      (corridors corridor-tile)))

(defn circular-room [floor-tile corridor-tile rng]
  "create room generator for circular rooms"
  (new-room-generator (circular-shape floor-tile)
                      (corridors corridor-tile)))

(defn circular-cache-room [floor-tile corridor-tile cache-tiles item-selector
                           character-selector rng]
  "create creator for circular rooms with cache"
  (new-room-generator (circular-shape floor-tile rng)
                      (cache-creator cache-tile center-tile item-selector
                                     character-selector)
                      (corridors corridor-tile)))

(defn circular-graveyard [floor-tile corridor-tile grave-tiles
                          item-selector character-selector rng]
  "create generator for circular graveyard"
  (new-room-generator (circular-shape floor-tile)
                      (add-rows)
                      (cache-creator grave-tiles (random-rows 75 rng)
                                     item-selector character-selector rng)
                      (corridors corridor-tile)))

(defn square-graveyard [floor-tile corridor-tile grave-tiles
                        item-selector character-selector rng]
  "create generator for square graveyard"
  (new-room-generator (square-shape floor-tile rng)
                      (add-rows)
                      (cache-creator grave-tiles (random-rows 75 rng)
                                     item-selector character-selector rng)
                      (corridors corridor-tile)))

(defn square-library [floor-tile corridor-tile bookshelf-tiles rng]
  "create generator for square library"
  (new-room-generator (square-shape floor-tile rng)
                      (add-rows)
                      (wall-creator bookshelf-tiles (random-rows 75 rng) rng)
                      (corridors corridor-tile)))

(defn circular-library [floor-tile corridor-tile bookshelf-tiles rng]
  "create generator for circular library"
  (new-room-generator (circular-shape floor-tile rng)
                      (add-rows)
                      (wall-creator bookshelf-tiles (random-rows 75 rng) rng)
                      (corridors corridor-tile)))

(defn square-pitroom [floor-tile corridor-tile pit-tile rng]
  "create generator for a square room with large pit in the middle"
  (new-room-generator (square-shape floor-tile rng)
                      (mark-center-area)
                      (trap-creator [pit-tile] PitTrap (center-area) rng)
                      (corridors corridor-tile)))

(defn skeletons [empty-pct character-generator rng]
  "create character selector for skeletons"
  (fn []
    (if (> (.randint rng 1 100) empty-pct)
      (let [[roll (.randint rng 1 100)]]
        (cond
         [true [(character-generator "skeleton warrior")]]))
      [])))

(defn mundane-items [empty-pct item-generator rng]
  "create item selector for mundane items"
  (fn []
    (if (> (.randint rng 1 100) empty-pct)
      (let [[roll (.randint rng 1 100)]]
        (cond
         [(> roll 40) [(.generate-item item-generator "club")]]
         [(> roll 20) [(.generate-item item-generator "dagger")]]
         [(> roll 10) [(.generate-item item-generator "axe")]]
         [true [(.generate-item item-generator "sword")]]))
      [])))
