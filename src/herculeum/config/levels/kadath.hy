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

(import [herculeum.config.room-generators [mundane-items skeletons]])

(level-config-dsl)

(level-list
 (new-level "upper kadath" 
            (room-list (square-room "ground_tile3" "ground_tile3")
                       (square-pitroom "ground_tile3" "ground_tile3"
                                       "rock_pit_07")
                       (circular-room "ground_tile3" "ground_tile3")
                       (circular-bones-room "ground_tile3" "ground_soil4" "ground_tile3"
                                            ["skull 1" "bones 1"] unlikely)
                       (circular-graveyard "ground_soil4" "ground_tile3"
                                           ["tomb 1" "tomb 2" "tomb 3" "tomb 4" "tomb 5"
                                            "tomb 6" "tomb 7" "tomb 8" "tomb 9"]
                                           (mundane-items 75 item-generator rng)
                                           (skeletons 50 creature-generator rng)))
            (layout (irregular-grid #t(80 40) #t(11 11))
                    (irregular-grid #t(40 80) #t(11 11)))
            (touch-up (wall-builder "wall_brick4")
                      (coarse-replace-floor "pattern 1" "ground_tile3" "ground_soil4")
                      (floor-builder "ground_tile3")
                      (floor-builder "ground_soil4")
                      (floor-swapper "ground_soil4" "ground_rock4" "pattern 2" unlikely)
                      (pit-builder "rock_pit")
                      (wall-cracker "wall_brick4" unlikely)
                      (support-beams "wall_brick4" "wooden beams" unlikely)                      
                      (coarse-replace-wall "pattern 3" "wall_brick4" "wall_rubble7"))
            (item-lists (option (item-by-type 1 2 "weapon")
                                (item-by-type 1 2 "armour")
                                (item-by-type 0 1 "tome")
                                (item-by-type 1 2 "potion"))
                        (option (item-by-type 2 4 "weapon")
                                (item-by-type 2 4 "armour")))
            (creature-lists (option (creature 1 2 "skeleton warrior"))
                            (option (creature 1 3 "rat")
                                    (creature 1 3 "fungus")))
            (connections (unique-stairs "second gate" "upper kadath"
                                        "grey stairs" "room" unlikely))
            "Ruins of ancient city are gloomy and silent"))
