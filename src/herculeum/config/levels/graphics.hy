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

(require [hy.extra.anaphoric [ap-each]])

(import [herculeum.ui.gui.resources]
        [PyQt4.QtCore [QRect]]
        [PyQt4.QtGui [QPixmap]])

(defn add-ground-set [gfx base]
  "add ground texture set"
  (.add-icon gfx base (+ ":ground/" base ".png") " ")
  (.add-icon gfx (+ base "_1") (+ ":ground/" base "_1.png") " ")
  (.add-icon gfx (+ base "_3") (+ ":ground/" base "_3.png") " ")
  (.add-icon gfx (+ base "_5") (+ ":ground/" base "_5.png") " ")
  (.add-icon gfx (+ base "_7") (+ ":ground/" base "_7.png") " ")
  (.add-icon gfx (+ base "_13") (+ ":ground/" base "_13.png") " ")
  (.add-icon gfx (+ base "_15") (+ ":ground/" base "_15.png") " ")
  (.add-icon gfx (+ base "_17") (+ ":ground/" base "_17.png") " ")
  (.add-icon gfx (+ base "_35") (+ ":ground/" base "_35.png") " ")
  (.add-icon gfx (+ base "_37") (+ ":ground/" base "_37.png") " ")
  (.add-icon gfx (+ base "_57") (+ ":ground/" base "_57.png") " ")
  (.add-icon gfx (+ base "_135") (+ ":ground/" base "_135.png") " ")
  (.add-icon gfx (+ base "_137") (+ ":ground/" base "_137.png") " ")
  (.add-icon gfx (+ base "_157") (+ ":ground/" base "_157.png") " ")
  (.add-icon gfx (+ base "_357") (+ ":ground/" base "_357.png") " ")
  (.add-icon gfx (+ base "_1357") (+ ":ground/" base "_1357.png") " "))

(defn add-wall-set [gfx base]
  "add wall texture set"
  (.add-icon gfx base (+ ":walls/" base ".png") "#")
  (.add-icon gfx (+ base "_13") (+ ":walls/" base "_13.png") "#")
  (.add-icon gfx (+ base "_15") (+ ":walls/" base "_15.png") "#")
  (.add-icon gfx (+ base "_17") (+ ":walls/" base "_17.png") "#")
  (.add-icon gfx (+ base "_35") (+ ":walls/" base "_35.png") "#")
  (.add-icon gfx (+ base "_37") (+ ":walls/" base "_37.png") "#")
  (.add-icon gfx (+ base "_57") (+ ":walls/" base "_57.png") "#")
  (.add-icon gfx (+ base "_135") (+ ":walls/" base "_135.png") "#")
  (.add-icon gfx (+ base "_137") (+ ":walls/" base "_137.png") "#")
  (.add-icon gfx (+ base "_157") (+ ":walls/" base "_157.png") "#")
  (.add-icon gfx (+ base "_357") (+ ":walls/" base "_357.png") "#")
  (.add-icon gfx (+ base "_1357") (+ ":walls/" base "_1357.png") "#"))

(defn add-pit-set [gfx base]
  "add pit texture set"
  (.add-icon gfx (+ base "_01") (+ ":pits/" base "_01.png") "^")
  (.add-icon gfx (+ base "_02") (+ ":pits/" base "_02.png") "^")
  (.add-icon gfx (+ base "_03") (+ ":pits/" base "_03.png") "^")
  (.add-icon gfx (+ base "_04") (+ ":pits/" base "_04.png") "^")
  (.add-icon gfx (+ base "_05") (+ ":pits/" base "_05.png") "^")
  (.add-icon gfx (+ base "_06") (+ ":pits/" base "_06.png") "^")
  (.add-icon gfx (+ base "_07") (+ ":pits/" base "_07.png") "^")
  (.add-icon gfx (+ base "_08") (+ ":pits/" base "_08.png") "^")
  (.add-icon gfx (+ base "_09") (+ ":pits/" base "_09.png") "^")
  (.add-icon gfx (+ base "_10") (+ ":pits/" base "_10.png") "^")
  (.add-icon gfx (+ base "_11") (+ ":pits/" base "_11.png") "^"))

(defn add-animated-tile [gfx base glyph]
  "add animated tile with two frames"
  (.add-icon gfx (+ base "_f0") (+ ":" base "_f0.png") glyph)
  (.add-icon gfx (+ base "_f1") (+ ":" base "_f1.png") glyph))

(defn init-graphics [context]
  "load graphcis"
  (let [gfx context.surface-manager]
    (load-ground-tiles gfx)
    (load-wall-tiles gfx)
    (load-pit-tiles gfx)
    (load-decoration-tiles gfx)
    (load-dungeon-features gfx)
    (load-items gfx)))

(defn add-ground-sets [gfx &rest sets]
  (ap-each sets (add-ground-set gfx it)))

(defn add-wall-sets [gfx &rest sets]
  (ap-each sets (add-wall-set gfx it)))

(defn add-pit-sets [gfx &rest sets]
  (ap-each sets (add-pit-set gfx it)))

(defn load-ground-tiles [gfx]
  "loads tiles used for ground"
  (.load-floor gfx (, 0 3) "ground_tile1")
  (.load-floor gfx (, 0 6) "ground_tile2")
  (.load-floor gfx (, 0 9) "ground_tile3")
  (.load-floor gfx (, 0 12) "ground_tile4")
  (.load-floor gfx (, 7 3) "ground_grass1")
  (.load-floor gfx (, 7 6) "ground_grass2")
  (.load-floor gfx (, 7 9) "ground_grass3")
  (.load-floor gfx (, 7 12) "ground_grass4")
  
  (add-ground-sets gfx
                   "ground_rock1" "ground_rock2" "ground_rock3" "ground_rock4"
                   "ground_soil1" "ground_soil2" "ground_soil3" "ground_soil4"
                   "ground_wood4"))

(defn load-wall-tiles [gfx]
  "load tiles used for walls"
  (add-wall-sets gfx
                 "wall_brick1" "wall_brick2" "wall_brick3" "wall_brick4"
                 "wall_rubble1" "wall_rubble2" "wall_rubble3" "wall_rubble4"
                 "wall_rubble5" "wall_rubble6" "wall_rubble7" "wall_rubble8"))

(defn load-pit-tiles [gfx]
  "load tiles used for pits"
  (add-pit-sets gfx
                "brick_pit" "rock_pit" "lava_pit_f0" "lava_pit_f1"))

(defn load-decoration-tiles [gfx]
  "load misc decorations"
  (.add-icon gfx "skull 1" ":decor/skull_1.png" " ")
  (.add-icon gfx "skull 2" ":decor/skull_2.png" " ")
  (.add-icon gfx "bones 1" ":decor/bones_1.png" " ")
  (.add-icon gfx "bones 2" ":decor/bones_2.png" " ")
  (.add-icon gfx "metal beams 1" ":decor/metal_beams_1" "#")
  (.add-icon gfx "metal beams 2" ":decor/metal_beams_2" "#")
  (.add-icon gfx "metal beams 3" ":decor/metal_beams_3" "#")
  (.add-icon gfx "metal beams 4" ":decor/metal_beams_4" "#")
  (.add-icon gfx "wooden beams 1" ":decor/wooden_beams_1.png" "#")
  (.add-icon gfx "wooden beams 2" ":decor/wooden_beams_2.png" "#")
  (.add-icon gfx "wooden beams 3" ":decor/wooden_beams_3.png" "#")
  (.add-icon gfx "wooden beams 4" ":decor/wooden_beams_4.png" "#")
  (.add-icon gfx "wall crack 1" ":decor/wall_crack_1.png" "#")
  (.add-icon gfx "wall crack 2" ":decor/wall_crack_2.png" "#")
  (.add-icon gfx "wall crack 3" ":decor/wall_crack_3.png" "#")
  (.add-icon gfx "wall crack 4" ":decor/wall_crack_4.png" "#")
  (.add-icon gfx "wall moss 1" ":decor/wall_moss_1.png" "#")
  (.add-icon gfx "wall moss 2" ":decor/wall_moss_2.png" "#")
  (.add-icon gfx "wall moss 3" ":decor/wall_moss_3.png" "#")
  (.add-icon gfx "wall moss 4" ":decor/wall_moss_4.png" "#")
  (add-animated-tile gfx "standing_candle" "|")
  (add-animated-tile gfx "fountain" "{")
  (add-animated-tile gfx "wall_torch" "|")
  (add-animated-tile gfx "wall_torches" "|"))

(defn load-dungeon-features [gfx]
  "load dungeon features like tombs, graves and such"
  (.add-icon gfx "tomb 1" ":tomb_1.png" "|")
  (.add-icon gfx "tomb 2" ":tomb_2.png" "|")
  (.add-icon gfx "tomb 3" ":tomb_3.png" "|")
  (.add-icon gfx "tomb 4" ":tomb_4.png" "|")
  (.add-icon gfx "tomb 5" ":tomb_5.png" "|")
  (.add-icon gfx "tomb 6" ":tomb_6.png" "|")
  (.add-icon gfx "tomb 7" ":tomb_7.png" "|")
  (.add-icon gfx "tomb 8" ":tomb_8.png" "|")
  (.add-icon gfx "tomb 9" ":tomb_9.png" "|")
  (.add-icon gfx "shelf 1" ":shelf_empty.png" "+")
  (.add-icon gfx "shelf 2" ":shelf_book_1.png" "+")
  (.add-icon gfx "shelf 3" ":shelf_book_2.png" "+")
  (.add-icon gfx "statue" ":decor/statue.png" "0")
  (.add-icon gfx "grey stairs down" ":misc/grey_stairs_down.png" ">")
  (.add-icon gfx "grey stairs up" ":misc/grey_stairs_up.png" "<"))

(defn load-items [gfx]
  "load item graphics"
  (.add-icon gfx "apple" ":items/apple.png" "%")
  (.add-icon gfx "tied-scroll" ":items/tied-scroll.png" "?")
  (.add-icon gfx "bag" ":items/bag.png" "(" ["dim" "red"])
  (.add-icon gfx "caltrops" ":traps/caltrops.png" "^" ["bright" "white"]))
