;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2015 Tuukka Turto
;;
;;  This file is part of pyherc.
;;
;;  pyherc is free software: you can redistribute it and/or modify
;;  it under the terms of the GNU General Public License as published by
;;  the Free Software Foundation either version 3 of the License or
;;  (at your option) any later version.
;;
;;  pyherc is distributed in the hope that it will be useful
;;  but WITHOUT ANY WARRANTY; without even the implied warranty of
;;  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;  GNU General Public License for more details.
;;
;;  You should have received a copy of the GNU General Public License
;;  along with pyherc.  If not see <http://www.gnu.org/licenses/>.

(require pyherc.macros)

(import [pyherc.generators.level [new-level]]
        [pyherc.generators.level.partitioners [binary-space-partitioning]]
        [pyherc.generators.level.decorator [wall-ornamenter]])
(import [herculeum.config.floor_builders [floor-builder wall-builder
                                          floor-swapper animated-pit-builder
                                          pit-builder]]
        [herculeum.config.room_generators [square-room square-pitroom]])

(defn init-level [rng item-generator creature-generator level-size context]
  [(new-level "upper mines" (rooms rng) (partitioners rng) (decorators rng)
              (item-adders rng) (creature-adders rng) (portal-configurations))])

(defn rooms [rng]
  [(square-room "ground_soil3" "ground_soil3" rng)
   (square-pitroom "ground_soil3" "ground_soil3" "lava_pit_f0_07" rng)
   (square-pitroom "ground_soil3" "ground_soil3" "rock_pit_07" rng)])

(defn partitioners [rng]
  [(binary-space-partitioning #t(80 40) #t(11 11) rng)])

(defn decorators [rng]
  [(wall-builder "wall_rubble2")
   (floor-builder "ground_soil3")
   (floor-swapper "ground_soil3" "ground_rock3" 25 rng)
   (pit-builder "rock_pit")
   (animated-pit-builder "lava_pit")
   (wall-ornamenter ["wall_rubble2_15" ["wall crack 4"]]
                    ["wall_rubble2_37" ["wall crack 1" "wall crack 2"]]
                    ["wall_rubble2_15" ["wall crack 3"]]
                    30 rng)
   (wall-ornamenter ["wall_rubble2_15" ["wooden beams 3"]]
                    ["wall_rubble2_37" ["wooden beams 1"]]
                    ["wall_rubble2_15" ["wooden beams 2"]]
                    30 rng)
   (wall-ornamenter nil
                    ["wall_rubble2_37" [["catacombs_torches_f0"
                                         "catacombs_torches_f1"]]]
                    nil
                    10 rng)])

(defn item-adders [rng]
  [])

(defn creature-adders [rng]
  [])

(defn portal-configurations []
  [])
