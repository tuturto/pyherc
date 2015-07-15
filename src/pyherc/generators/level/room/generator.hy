;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2015 Tuukka Turto
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

(import [random])
(import [pyherc.data [distance-between]]
        [pyherc.generators.level.partitioners [section-floor
                                               section-data]]
        [pyherc.generators.level.room.corridor [corridors]]
        [pyherc.generators.level.room.shapes [circular-shape
                                              square-shape]]
        [pyherc.generators.level.room.overlays [add-rows
                                                add-columns]])

(defn new-room-generator [&rest creators]
  "create a room generator"
  (fn [section]
    (ap-each creators (it section))))

(defn tomes-and-potions-cache [item-generator]
  "create cache content creator"
  (fn []
    []))

(defn no-characters-cache [character-generator]
  "create cache character creator"
  (fn []
    []))

(defn fill-columns [tile]
  (fn [section]
    (ap-each (section-data section "columns") (section-floor section it tile))))

(defn fill-rows [tile]
  (fn [section]
    (ap-each (section-data section "rows") (section-floor section it tile))))
