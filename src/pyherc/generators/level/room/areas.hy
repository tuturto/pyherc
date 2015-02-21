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
(require hy.macros)

(import [pyherc.generators.level.partitioners [section-data]])

(defn center-tile [section]
  "select center tile of section"
  [(section-data section :center-point)])

(defn random-rows [percentage rng]
  "create selector for picking random row tiles"
  (fn [section]
    (ap-each (section-data section :rows)
             (when (<= (.randint rng 1 100) percentage)
               (yield it)))))

(defn random-columns [percentage rng]
  "create selector for picking random column tiles"
  (fn [section]
    (ap-each (section-data section :columns)
             (when (<= (.randint rng 1 100) percentage)
               (yield it)))))

(defn center-area []
  "create selector for picking center area of room"
  (fn [section]
    (ap-each (section-data section :center-area)
             (yield it))))

(defn side-by-side [area]
  "create selector for picking tiles side by side"
  (fn [section]
    (ap-each (area section) 
             (do 
              (yield (, (+ (first it) 1) (second it)))
              (yield (, (- (first it) 1) (second it)))))))
