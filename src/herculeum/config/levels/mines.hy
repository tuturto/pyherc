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

(require hy.contrib.anaphoric)
(require pyherc.macros)
(require herculeum.config.room-generators)

(import [pyherc.data.probabilities [*]]
        [pyherc.data.traps [PitTrap]]        
        [pyherc.generators.level [new-level item-by-type item-lists
                                  creature-lists creature]]
        [pyherc.generators.level.partitioners [binary-space-partitioning]])
(import [herculeum.config.floor-builders [floor-builder wall-builder
                                          floor-swapper animated-pit-builder
                                          pit-builder wall-cracker
                                          support-beams wall-torches]]
        [herculeum.config.portals [normal-stairs special-stairs]]
        [herculeum.config.room-generators [square-room square-pitroom]])

(level-config-dsl)

(level-list
 (new-level "upper mines" 
            (room-list (square-room* "ground_soil3" "ground_soil3")
                       (square-pitroom* "ground_soil3" "ground_soil3"
                                        "rock_pit_07"))
            (layout (binary-space-partitioning* #t(80 40) #t(11 11))
                    (binary-space-partitioning* #t(40 80) #t(11 11)))
            (touch-up (wall-builder "wall_rubble2")
                      (floor-builder "ground_soil3")
                      (floor-swapper* "ground_soil3" "ground_rock3" unlikely)
                      (pit-builder "rock_pit")
                      (wall-cracker* "wall_rubble2" unlikely)
                      (support-beams* "wall_rubble2" "wooden beams" unlikely)
                      (wall-torches* "wall_rubble2" almost-certainly-not))
            (item-lists* (option (item-by-type 1 2 "weapon")
                                 (item-by-type 1 2 "armour")
                                 (item-by-type 0 1 "tome")
                                 (item-by-type 1 2 "potion"))
                         (option (item-by-type 2 4 "weapon")
                                 (item-by-type 2 4 "armour")))
            (creature-lists* (option (creature 1 2 "skeleton warrior"))
                             (option (creature 1 3 "rat")
                                     (creature 1 3 "fungus" "corridor")))
            (connections (special-stairs "first gate" "upper mines" 
                                         "room" unlikely)
                         (normal-stairs "upper mines" "lower mines" 
                                        "room" certainly)))
 (new-level "lower mines" 
            (room-list (square-room* "ground_soil3" "ground_soil3")
                       (square-pitroom* "ground_soil3" "ground_soil3" 
                                        "lava_pit_f0_07")
                       (square-pitroom* "ground_soil3" "ground_soil3"
                                        "rock_pit_07"))
            (layout (binary-space-partitioning* #t(80 40) #t(11 11))
                    (binary-space-partitioning* #t(40 80) #t(11 11)))
            (touch-up (wall-builder "wall_rubble2")
                      (floor-builder "ground_soil3")
                      (floor-swapper* "ground_soil3" "ground_rock3" unlikely)
                      (pit-builder "rock_pit")
                      (animated-pit-builder "lava_pit")
                      (wall-cracker* "wall_rubble2" unlikely)
                      (support-beams* "wall_rubble2" "wooden beams" unlikely)
                      (wall-torches* "wall_rubble2" almost-certainly-not))
            (item-lists* (option (item-by-type 1 2 "weapon")
                                 (item-by-type 1 2 "armour")
                                 (item-by-type 0 1 "tome")
                                 (item-by-type 1 2 "potion"))
                         (option (item-by-type 2 4 "weapon")
                                 (item-by-type 2 4 "armour")))
            (creature-lists* (option (creature 1 2 "skeleton warrior"))
                             (option (creature 1 3 "rat")
                                     (creature 1 3 "fungus" "corridor")))
            (connections (normal-stairs "lower mines" "forge" 
                                        "room" certainly)))
 (new-level "forge" 
            (room-list (square-room* "ground_soil3" "ground_soil3")
                       (square-pitroom* "ground_soil3" "ground_soil3" 
                                        "lava_pit_f0_07"))
            (layout (binary-space-partitioning* #t(80 40) #t(11 11))
                    (binary-space-partitioning* #t(40 80) #t(11 11)))
            (touch-up (wall-builder "wall_rubble2")
                      (floor-builder "ground_soil3")
                      (floor-swapper* "ground_soil3" "ground_rock3" unlikely)
                      (pit-builder "rock_pit")
                      (animated-pit-builder "lava_pit")
                      (wall-cracker* "wall_rubble2" unlikely)
                      (support-beams* "wall_rubble2" "wooden beams" unlikely)
                      (wall-torches* "wall_rubble2" almost-certainly-not))
            (item-lists* (option (item-by-type 1 2 "weapon")
                                 (item-by-type 1 2 "armour")
                                 (item-by-type 0 1 "tome")
                                 (item-by-type 1 2 "potion"))
                         (option (item-by-type 2 4 "weapon")
                                 (item-by-type 2 4 "armour")))
            (creature-lists* (option (creature 1 2 "skeleton warrior"))
                             (option (creature 1 3 "rat")
                                     (creature 1 3 "fungus" "corridor")))
            []))
