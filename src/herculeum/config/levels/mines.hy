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
(require pyherc.config.dsl.level)

(level-config-dsl)

(level-list
 (new-level "upper mines" 
            (room-list (square-room "ground_soil2" "ground_soil2")
                       (square-pitroom "ground_soil2" "ground_soil2"
                                       "rock_pit_07"))
            (layout (irregular-grid #t(80 40) #t(11 11))
                    (irregular-grid #t(40 80) #t(11 11)))
            (touch-up (wall-builder "wall_rubble2")
                      (coarse-replace-floor "pattern 1" "ground_soil2" "ground_soil3")
                      (floor-builder "ground_soil2")
                      (floor-builder "ground_soil3")
                      (floor-swapper "ground_soil2" "ground_rock2" unlikely)
                      (floor-swapper "ground_soil3" "ground_rock3" unlikely)
                      (pit-builder "rock_pit")
                      (wall-cracker "wall_rubble2" unlikely)
                      (support-beams "wall_rubble2" "wooden beams" unlikely)
                      (wall-torches "wall_rubble2" almost-certainly-not)
                      (coarse-replace-wall "pattern 1" "wall_rubble2" "wall_rubble3"))
            (item-lists (option (item-by-type 1 2 "weapon")
                                (item-by-type 1 2 "armour")
                                (item-by-type 0 1 "tome")
                                (item-by-type 1 2 "potion"))
                        (option (item-by-type 2 4 "weapon")
                                (item-by-type 2 4 "armour")))
            (creature-lists (option (creature 1 2 "skeleton warrior"))
                            (option (creature 1 3 "rat")
                                    (creature 1 3 "fungus")))
            (connections (unique-stairs "first gate" "upper mines"
                                        "grey stairs" "room" unlikely)
                         (unique-stairs "upper mines" "lower mines"
                                        "grey stairs" "room" certainly))
            "Mines are full of smoke and noise of rock being shattered.")
 (new-level "lower mines" 
            (room-list (square-room "ground_soil3" "ground_soil3")
                       (square-pitroom "ground_soil3" "ground_soil3" 
                                       "lava_pit_f0_07")
                       (square-pitroom "ground_soil3" "ground_soil3"
                                       "rock_pit_07"))
            (layout (irregular-grid #t(80 40) #t(11 11))
                    (irregular-grid #t(40 80) #t(11 11)))
            (touch-up (wall-builder "wall_rubble2")
                      (floor-builder "ground_soil3")
                      (floor-swapper "ground_soil3" "ground_rock3" unlikely)
                      (pit-builder "rock_pit")
                      (animated-pit-builder "lava_pit")
                      (wall-cracker "wall_rubble2" unlikely)
                      (support-beams "wall_rubble2" "wooden beams" unlikely)
                      (wall-torches "wall_rubble2" almost-certainly-not))
            (item-lists (option (item-by-type 1 2 "weapon")
                                (item-by-type 1 2 "armour")
                                (item-by-type 0 1 "tome")
                                (item-by-type 1 2 "potion"))
                        (option (item-by-type 2 4 "weapon")
                                (item-by-type 2 4 "armour")))
            (creature-lists (option (creature 1 2 "skeleton warrior"))
                            (option (creature 1 3 "rat")
                                     (creature 1 3 "fungus")))
            (connections (unique-stairs "lower mines" "forge" 
                                        "grey stairs" "room" certainly))
            "Mines are full of smoke and noise of rock being shattered.")
 (new-level "forge" 
            (room-list (square-room "ground_soil3" "ground_soil3")
                       (square-pitroom "ground_soil3" "ground_soil3" 
                                       "lava_pit_f0_07"))
            (layout (irregular-grid #t(80 40) #t(11 11))
                    (irregular-grid #t(40 80) #t(11 11)))
            (touch-up (wall-builder "wall_rubble2")
                      (floor-builder "ground_soil3")
                      (floor-swapper "ground_soil3" "ground_rock3" unlikely)
                      (pit-builder "rock_pit")
                      (animated-pit-builder "lava_pit")
                      (wall-cracker "wall_rubble2" unlikely)
                      (support-beams "wall_rubble2" "wooden beams" unlikely)
                      (wall-torches "wall_rubble2" almost-certainly-not))
            (item-lists (option (item-by-type 1 2 "weapon")
                                (item-by-type 1 2 "armour")
                                (item-by-type 0 1 "tome")
                                (item-by-type 1 2 "potion"))
                        (option (item-by-type 2 4 "weapon")
                                (item-by-type 2 4 "armour")))
            (creature-lists (option (creature 1 2 "skeleton warrior"))
                            (option (creature 1 3 "rat")
                                    (creature 1 3 "fungus")))
            []
            "Heat radiates from the forge."))
