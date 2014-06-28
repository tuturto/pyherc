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

(import [pyherc.generators.level.room [new-room-generator square-shape
                                       circular-shape corridors
                                       add-rows cache-creator
                                       random-rows]])

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
  "create generator for circular graveyard"
  (new-room-generator (square-shape floor-tile rng)
                      (add-rows)
                      (cache-creator grave-tiles (random-rows 75 rng)
                                     item-selector character-selector rng)
                      (corridors corridor-tile)))
