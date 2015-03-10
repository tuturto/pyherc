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

(require pyherc.macros)

(defmacro level-config-dsl []
  `(import [herculeum.config.floor-builders [floor-builder wall-builder
                                             animated-pit-builder
                                             pit-builder
                                             wall-torches
                                             aggregate-decorator]]
           [pyherc.data.probabilities [*]]
           [pyherc.data.traps [PitTrap]]
           [pyherc.generators.level [new-level
                                     PortalAdderConfiguration]]
           [pyherc.generators.level.creatures [CreatureAdder]]
           [pyherc.generators.level.decorator [FloorBuilderDecorator
                                               FloorBuilderDecoratorConfig
                                               SurroundingDecorator
                                               SurroundingDecoratorConfig
                                               DirectionalWallDecorator
                                               DirectionalWallDecoratorConfig
                                               floor-swap wall-ornamenter]]
           [pyherc.generators.level.item [ItemAdder]]
           [pyherc.generators.level.partitioners [binary-space-partitioning]]
           [pyherc.generators.level.room [new-room-generator square-shape
                                          circular-shape corridors
                                          add-rows cache-creator
                                          mark-center-area
                                          random-rows trap-creator
                                          wall-creator floor-creator
                                          ornament-creator
                                          center-area center-tile side-by-side
                                          random-pillars]]))

(defmacro room-list [&rest rooms]
  `[~@rooms])

(defmacro layout [&rest partitions]
  `[~@partitions])

(defmacro touch-up [&rest decorators]
  `[~@decorators])

(defmacro connections [&rest portals]
  `[~@portals])

(defmacro option [&rest elements]
  `[~@elements])

(defmacro level-list [&rest levels]
  `(defn init-level [rng item-generator creature-generator level-size context]
     [~@levels]))

(defmacro floor-swapper [source destination chance]
  `(aggregate-decorator (floor-swap (+ ~source "_1357") ~destination
                                    ~chance rng)
                        (floor-builder ~destination)))

(defmacro support-beams [wall beam chance]
  `(wall-ornamenter [(+ ~wall "_15") [(+ ~beam " 3")]]
                    [(+ ~wall "_37") [(+ ~beam " 1")]]
                    [(+ ~wall "_15") [(+ ~beam " 2")]]
                    ~chance rng))

(defmacro wall-cracker [wall chance]
  `(wall-ornamenter [(+ ~wall "_15") ["wall crack 4"]]
                    [(+ ~wall "_37") ["wall crack 1" "wall crack 2"]]
                    [(+ ~wall "_15") ["wall crack 3"]]
                    ~chance rng))

(defmacro wall-torches [wall chance]
  `(wall-ornamenter nil
                    [(+ ~wall "_37") [["wall_torches_f0"
                                       "wall_torches_f1"]
                                      ["wall_torch_f0"
                                       "wall_torch_f1"]]]
                    nil
                    ~chance rng))

(defmacro item-lists [&rest items]
  `(ap-map (ItemAdder item-generator it rng) [~@items]))

(defmacro item-by-type [min-amount max-amount item-type]
  `{"min_amount" ~min-amount "max_amount" ~max-amount "name" nil
                 "type" ~item-type "location" "room"})

(defmacro item-by-name [min-amount max-amount name]
  `{"min_amount" ~min-amount "max_amount" ~max-amount "name" ~name
                 "type" nil "location" "room"})

(defmacro creature-lists [&rest creatures]
  `(ap-map (CreatureAdder creature-generator it rng) [~@creatures]))

(defmacro creature [min-amount max-amount name]
  {"min_amount" min-amount "max_amount" max-amount "name" name
   "location" "room"})

(defmacro square-room [floor-tile corridor-tile]
  `(new-room-generator (square-shape ~floor-tile rng)
                       (corridors ~corridor-tile)))

(defmacro square-pitroom [floor-tile corridor-tile pit-tile]
  `(new-room-generator (square-shape ~floor-tile rng)
                       (mark-center-area)
                       (trap-creator [~pit-tile] PitTrap (center-area) rng)
                       (corridors ~corridor-tile)))

(defmacro irregular-grid [level-size room-size]
  `(binary-space-partitioning ~level-size ~room-size rng))

(defmacro unique-stairs [origin destination base-tile location-type chance]
  `(PortalAdderConfiguration #t((+ ~base-tile " up") (+ ~base-tile " down"))
                             ~origin ~location-type ~chance
                             ~destination true))

(defmacro common-stairs [origin destination base-tile location-type chance]
  `(PortalAdderConfiguration #t((+ ~base-tile " up") (+ ~base-tile " down"))
                             ~origin ~location-type ~chance
                             ~destination false))

(defmacro pillar-room [floor-tile corridor-tile pillar-tiles]
  `(new-room-generator (square-shape ~floor-tile rng)
                       (wall-creator ~pillar-tiles
                                     (random-pillars 100 rng) rng)
                       (corridors ~corridor-tile)))

(defmacro square-band-room [floor-tile edge-tile corridor-tile]
  `(new-room-generator (square-shape ~edge-tile rng)
                       (mark-center-area)
                       (floor-creator [~floor-tile] (center-area) rng)
                       (corridors ~corridor-tile)))

(defmacro square-banded-library [floor-tile edge-tile corridor-tile 
                                 bookshelf-tiles]
  `(new-room-generator (square-shape ~edge-tile rng)
                       (mark-center-area)
                       (add-rows)
                       (floor-creator [~floor-tile] (center-area) rng)
                       (wall-creator ~bookshelf-tiles (random-rows 90 rng) rng)
                       (corridors ~corridor-tile)))

(defmacro circular-room [floor-tile corridor-tile]
  `(new-room-generator (circular-shape ~floor-tile)
                       (corridors ~corridor-tile)))

(defmacro circular-band-room [floor-tile edge-tile corridor-tile]
  `(new-room-generator (circular-shape ~edge-tile)
                       (mark-center-area)
                       (floor-creator [~floor-tile] (center-area) rng)
                       (corridors ~corridor-tile)))

(defmacro circular-cache-room [floor-tile corridor-tile cache-tiles
                               item-selector character-selector]
  `(new-room-generator (circular-shape ~floor-tile)
                       (cache-creator ~cache-tiles center-tile ~item-selector
                                      ~character-selector rng)
                       (corridors ~corridor-tile)))

(defmacro circular-room-with-candles [floor-tile edge-tile corridor-tile
                                      candle-tiles]
  `(new-room-generator (circular-shape ~edge-tile)
                       (mark-center-area)
                       (floor-creator [~floor-tile] (center-area) rng)
                       (ornament-creator ~candle-tiles 
                                         (side-by-side center-tile) 
                                         100 rng)
                       (corridors ~corridor-tile)))

(defmacro circular-graveyard [floor-tile corridor-tile grave-tiles
                              item-selector character-selector]
  `(new-room-generator (circular-shape ~floor-tile)
                       (add-rows)
                       (cache-creator ~grave-tiles (random-rows 75 rng)
                                      ~item-selector ~character-selector rng)
                       (corridors ~corridor-tile)))

(defmacro square-graveyard [floor-tile corridor-tile grave-tiles
                        item-selector character-selector]
  `(new-room-generator (square-shape ~floor-tile rng)
                       (add-rows)
                       (cache-creator ~grave-tiles (random-rows 75 rng)
                                     ~item-selector ~character-selector rng)
                       (corridors ~corridor-tile)))

(defmacro square-library [floor-tile corridor-tile bookshelf-tiles]
  `(new-room-generator (square-shape ~floor-tile rng)
                       (add-rows)
                       (wall-creator ~bookshelf-tiles (random-rows 75 rng) rng)
                       (corridors ~corridor-tile)))

(defmacro circular-library [floor-tile corridor-tile bookshelf-tiles]
  `(new-room-generator (circular-shape ~floor-tile)
                       (add-rows)
                       (wall-creator ~bookshelf-tiles (random-rows 90 rng) rng)
                       (corridors ~corridor-tile)))

(defmacro square-pitroom [floor-tile corridor-tile pit-tile]
  `(new-room-generator (square-shape ~floor-tile rng)
                       (mark-center-area)
                       (trap-creator [~pit-tile] PitTrap (center-area) rng)
                       (corridors ~corridor-tile)))

(defmacro circular-pitroom [floor-tile corridor-tile pit-tile]
  `(new-room-generator (circular-shape ~floor-tile)
                       (mark-center-area)
                       (trap-creator [~pit-tile] PitTrap (center-area) rng)
                       (corridors ~corridor-tile)))

(defmacro circular-bones-room [floor-tile edge-tile corridor-tile bones rate]
  `(new-room-generator (circular-shape ~edge-tile)
                       (mark-center-area)
                       (floor-creator [~floor-tile] (center-area) rng)
                       (ornament-creator ~bones (center-area) ~rate rng)
                       (corridors ~corridor-tile)))

(defn no-characters []
  "create character selector for nothing"
  (fn []
    []))

(defn skeletons [empty-pct character-generator rng]
  "create character selector for skeletons"
  (fn []
    (if (> (.randint rng 1 100) empty-pct)
      (let [[roll (.randint rng 1 100)]]
        (cond
         [true [(character-generator "skeleton warrior")]]))
      [])))

(defn no-items []
  "create item selector for nothing"
  (fn []
    []))

(defn altar-items [empty-pct item-generator rng]
  "create item selector for items found on common altars"
  (fn []
    (if (> (.randint rng 1 100) empty-pct)
      (let [[roll (.randint rng 1 100)]]
        (cond
         [(> roll 50) [(.generate-item item-generator "robes")]]
         [true [(.generate-item item-generator nil "tome")]]))
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
