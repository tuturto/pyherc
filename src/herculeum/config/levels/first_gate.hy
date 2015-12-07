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
 (level "first gate"
        #s("The first gate is where your long journey begins. This is perfect"
           "area for gathering some supplies before venturing further in the"
           "caves.")
        (connections (unique-stairs "first gate" "lower caverns"
                                    "grey stairs" "room" certainly))
        (layout (regular-grid #t(20 20) #t(10 10))
                (regular-grid #t(20 10) #t(10 10))
                (regular-grid #t(10 20) #t(10 10)))
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
                            (item-by-type 1 1 "hint")
                            (item-by-type 0 2 "boots")))))
