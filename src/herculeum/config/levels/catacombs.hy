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
 (new-level "lower catacombs"
            (room-list (circular-room "ground_tile3" "ground_soil4")
                       (circular-band-room "ground_wood4" "ground_soil4"
                                           "ground_soil4")
                       (square-room "ground_tile3" "ground_soil4")
                       (square-room "ground_soil4" "ground_soil4")
                       (circular-room-with-candles "ground_wood4"
                                                   "ground_soil4"
                                                   "ground_soil4"
                                                   [["standing_candle_f0"
                                                     "standing_candle_f1"]]))
            (layout (irregular-grid #t(40 40) #t(11 11)))
            (touch-up (wall-builder "wall_rubble6")
                      (floor-builder "ground_soil4")
                      (floor-builder "ground_soil3")
                      (floor-builder "ground_tile3")
                      (floor-builder "ground_tile4")
                      (floor-builder "ground_wood4")
                      (wall-cracker "wall_rubble6" unlikely)
                      (support-beams "wall_rubble6" "wooden beams" unlikely)
                      (wall-torches "wall_rubble6" almost-certainly-not))
            (item-lists (option (item-by-type 2 3 "weapon")
                                (item-by-type 2 3 "armour")
                                (item-by-type 2 4 "potion")
                                (item-by-type 1 4 "food")))
            (creature-lists (option (creature 1 3 "rat")))
            (connections (unique-stairs "lower catacombs" "central catacombs"
                                        "grey stairs" "room" certainly))
            "Dark and damp catacombs stretch to all directions.")
 (new-level "central catacombs"
            (room-list (circular-room "ground_tile3" "ground_soil4")
                       (circular-band-room "ground_wood4" "ground_soil4"
                                           "ground_soil4")
                       (square-room "ground_tile3" "ground_soil4")
                       (square-room "ground_soil4" "ground_soil4")
                       (circular-room-with-candles "ground_wood4"
                                                   "ground_soil4"
                                                   "ground_soil4"
                                                   [["standing_candle_f0"
                                                     "standing_candle_f1"]]))
            (layout (irregular-grid #t(40 40) #t(11 11)))
            (touch-up (wall-builder "wall_rubble6")
                      (floor-builder "ground_soil4")
                      (floor-builder "ground_soil3")
                      (floor-builder "ground_tile3")
                      (floor-builder "ground_tile4")
                      (floor-builder "ground_wood4")
                      (wall-cracker "wall_rubble6" unlikely)
                      (support-beams "wall_rubble6" "wooden beams" unlikely)
                      (wall-torches "wall_rubble6" almost-certainly-not))
            (item-lists (option (item-by-type 2 3 "weapon")
                                (item-by-type 2 3 "armour")
                                (item-by-type 2 4 "potion")
                                (item-by-type 1 4 "food")
                                (item-by-type 0 2 "hint")))
            (creature-lists (option (creature 1 3 "rat")))
            (connections (unique-stairs "central catacombs" "upper catacombs"
                                        "grey stairs" "room" certainly))
            "Dark and damp catacombs stretch to all directions.")
 (new-level "upper catacombs"
            (room-list (circular-room "ground_tile3" "ground_soil4")
                       (circular-band-room "ground_wood4" "ground_soil4"
                                           "ground_soil4")
                       (square-room "ground_tile3" "ground_soil4")
                       (square-room "ground_soil4" "ground_soil4")
                       (circular-room-with-candles "ground_wood4"
                                                   "ground_soil4"
                                                   "ground_soil4"
                                                   [["standing_candle_f0"
                                                     "standing_candle_f1"]]))
            (layout (irregular-grid #t(40 40) #t(11 11)))
            (touch-up (wall-builder "wall_rubble6")
                      (floor-builder "ground_soil4")
                      (floor-builder "ground_soil3")
                      (floor-builder "ground_tile3")
                      (floor-builder "ground_tile4")
                      (floor-builder "ground_wood4")
                      (wall-cracker "wall_rubble6" unlikely)
                      (support-beams "wall_rubble6" "wooden beams" unlikely)
                      (wall-torches "wall_rubble6" almost-certainly-not))
            (item-lists (option (item-by-type 2 3 "weapon")
                                (item-by-type 2 3 "armour")
                                (item-by-type 2 4 "potion")
                                (item-by-type 1 4 "food")))
            (creature-lists (option (creature 1 3 "rat")))
            (connections (unique-stairs "upper catacombs" "final gate"
                                        "grey stairs" "room" certainly))
            "Dark and damp catacombs stretch to all directions."))
