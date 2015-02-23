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

(defn add-animated-tile [gfx base glyph]
  "add animated tile with two frames"
  (.add-icon gfx (+ base "_f0") (+ ":" base "_f0.png") glyph)
  (.add-icon gfx (+ base "_f1") (+ ":" base "_f1.png") glyph))

(defn init-graphics [context]
  "load graphcis"
  (let [[gfx context.surface-manager]]
    (load-ground-tiles gfx)
    (load-decoration-tiles gfx)
    (load-dungeon-features gfx)))

(defn add-ground-sets [gfx &rest sets]
  (ap-each sets (add-ground-set gfx it)))

(defn load-ground-tiles [gfx]
  "loads tiles used for ground"
  (add-ground-sets gfx
                   "ground_rock1" "ground_rock2" "ground_rock3" "ground_rock4"
                   "ground_soil1" "ground_soil2" "ground_soil3" "ground_soil4"
                   "ground_tile3" "ground_tile4"
                   "ground_wood4"))

(defn load-decoration-tiles [gfx]
  "load misc decorations"
  (.add-icon gfx "skull 1" ":decor/skull_1.png" " ")
  (.add-icon gfx "skull 2" ":decor/skull_2.png" " ")
  (.add-icon gfx "bones 1" ":decor/bones_1.png" " ")
  (.add-icon gfx "bones 2" ":decor/bones_2.png" " ")
  (add-animated-tile gfx "standing_candle" "|")
  (add-animated-tile gfx "fountain" "{"))

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
  (.add-icon gfx "shelf 3" ":shelf_book_2.png" "+"))

