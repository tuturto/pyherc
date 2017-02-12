;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2017 Tuukka Turto
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

(require [pyherc.macros [*]])
(require [pyherc.config.dsl.level [*]])

(import [herculeum.config.room-generators [mundane-items skeletons]])

(level-config-dsl)

(level-list
 (level "upper kadath" 
        "Ruins of ancient city are gloomy and silent"
        (room-list (square-room "ground_tile3" "ground_tile3")
                   (square-pitroom "ground_tile3" "ground_tile3"
                                   "rock_pit_07")
                   (circular-room "ground_tile3" "ground_tile3")
                   (circular-bones-room "ground_tile3" "ground_soil4" "ground_tile3"
                                        ["skull 1" "skull 2" "bones 1" "bones 2"] unlikely)
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
                                    "grey stairs" "room" unlikely))))
