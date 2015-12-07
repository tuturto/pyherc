;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2015 Tuukka Turto
;; 
;; Permission is hereby granted, free of charge, to any person obtaining a copy
;; of this software and associated documentation files (the "Software"), to deal
;; in the Software without restriction, including without limitation the rights
;; to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
;; copies of the Software, and to permit persons to whom the Software is
;; furnished to do so, subject to the following conditions:
;; 
;; The above copyright notice and this permission notice shall be included in
;; all copies or substantial portions of the Software.
;; 
;; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
;; IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
;; FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
;; AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
;; LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
;; OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
;; THE SOFTWARE.

(require pyherc.macros)
(require pyherc.config.dsl.level)

(level-config-dsl)

(level-list
 (level "upper mines" 
        "Mines are full of smoke and noise of rock being shattered."
        (room-list (square-room "ground_soil2" "ground_soil2")
                   (square-pitroom "ground_soil2" "ground_soil2"
                                   "rock_pit_07"))
        (layout (irregular-grid #t(80 40) #t(11 11))
                (irregular-grid #t(40 80) #t(11 11)))
        (touch-up (wall-builder "wall_rubble2")
                  (coarse-replace-floor "pattern 1" "ground_soil2" "ground_soil3")
                  (floor-builder "ground_soil2")
                  (floor-builder "ground_soil3")
                  (floor-swapper "ground_soil2" "ground_rock2" "pattern 2" unlikely)
                  (floor-swapper "ground_soil3" "ground_rock3" "pattern 3" unlikely)
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
                                    "grey stairs" "room" certainly)))
 (level "lower mines" 
        "Mines are full of smoke and noise of rock being shattered."
        (room-list (square-room "ground_soil3" "ground_soil3")
                   (square-pitroom "ground_soil3" "ground_soil3" 
                                   "lava_pit_f0_07")
                   (square-pitroom "ground_soil3" "ground_soil3"
                                   "rock_pit_07"))
        (layout (irregular-grid #t(80 40) #t(11 11))
                (irregular-grid #t(40 80) #t(11 11)))
        (touch-up (wall-builder "wall_rubble2")
                  (floor-builder "ground_soil3")
                  (floor-swapper "ground_soil3" "ground_rock3" "pattern 1" unlikely)
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
                                    "grey stairs" "room" certainly)))
 (level "forge" 
        "Heat radiates from the forge."
        (room-list (square-room "ground_soil3" "ground_soil3")
                   (square-pitroom "ground_soil3" "ground_soil3" 
                                   "lava_pit_f0_07"))
        (layout (irregular-grid #t(80 40) #t(11 11))
                (irregular-grid #t(40 80) #t(11 11)))
        (touch-up (wall-builder "wall_rubble2")
                  (floor-builder "ground_soil3")
                  (floor-swapper "ground_soil3" "ground_rock3" "pattern 1" unlikely)
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
                                (creature 1 3 "fungus")))))
