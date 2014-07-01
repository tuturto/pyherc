;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2014 Tuukka Turto
;;
;;  This file is part of pyherc.
;;
;;  pyherc is free software: you can redistribute it and/or modify
;;  it under the terms of the GNU General Public License as published by
;;  the Free Software Foundation, either version 3 of the License, or
;;  (at your option) any later version.
;;
;;  pyherc is distributed in the hope that it will be useful,
;;  but WITHOUT ANY WARRANTY; without even the implied warranty of
;;  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;  GNU General Public License for more details.
;;
;;  You should have received a copy of the GNU General Public License
;;  along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

(require hy.contrib.anaphoric)
(require pyherc.macros)

(import [pyherc.data [blocks-movement distance-between area-around]]
        [pyherc.generators.level.partitioners [section-floor section-wall
                                               section-data section-connections
                                               section-to-map section-level]])

(defn add-rows []
  "create generator for pre-placing rows"
  (fn [section]
    (let [[even-tiles []]
          [odd-tiles []]]
      (ap-each (section-data section :room-tiles)
               (when (free-around? section it)
                 (if (odd? (second it)) (.append odd-tiles it)
                     (.append even-tiles it))))
      (section-data section :even-rows even-tiles)
      (section-data section :odd-rows odd-tiles)
      (if (> (len even-tiles) (len odd-tiles))
        (section-data section :rows even-tiles)
        (section-data section :rows odd-tiles)))))

(defn add-columns []
  "create generator for pre-placing columns"
  (fn [section]
    (let [[even-tiles []]
          [odd-tiles []]]
      (ap-each (section-data section :room-tiles)
               (when (free-around? section it)
                 (if (odd? (first it)) (.append odd-tiles it)
                     (.append even-tiles it))))
      (section-data section :even-columns even-tiles)
      (section-data section :odd-columns odd-tiles)
      (if (> (len even-tiles) (len odd-tiles))
        (section-data section :columns even-tiles)
        (section-data section :columns odd-tiles)))))

(defn mark-center-area []
  "create generator to mark center area of room"
  (fn [section]
    (let [[center-tiles []]]
      (ap-each (section-data section :room-tiles)
               (when (free-around? section it)
                 (.append center-tiles it)))
      (section-data section :center-area center-tiles))))

(defn free-around? [section location]
  "are tiles around given section location free?"
  (let [[tiles (list (area-around (section-to-map section location)))]
        [level (section-level section)]
        [non-blocking (list (ap-map (not (blocks-movement level it)) tiles))]]
    (ap-reduce (and it acc) (list non-blocking))))
