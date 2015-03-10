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

(defn no-characters []
  "create character selector for nothing"
  (fn []
    []))

(defn skeletons [empty-pct character-generator rng]
  "create character selector for skeletons"
  (fn []
    (if (> (.randint rng 1 100) empty-pct)
      (let [[roll (.randint rng 1 100)]]
        (cond
         [true [(character-generator "skeleton warrior")]]))
      [])))

(defn no-items []
  "create item selector for nothing"
  (fn []
    []))

(defn altar-items [empty-pct item-generator rng]
  "create item selector for items found on common altars"
  (fn []
    (if (> (.randint rng 1 100) empty-pct)
      (let [[roll (.randint rng 1 100)]]
        (cond
         [(> roll 50) [(.generate-item item-generator "robes")]]
         [true [(.generate-item item-generator nil "tome")]]))
      [])))

(defn mundane-items [empty-pct item-generator rng]
  "create item selector for mundane items"
  (fn []
    (if (> (.randint rng 1 100) empty-pct)
      (let [[roll (.randint rng 1 100)]]
        (cond
         [(> roll 40) [(.generate-item item-generator "club")]]
         [(> roll 20) [(.generate-item item-generator "dagger")]]
         [(> roll 10) [(.generate-item item-generator "axe")]]
         [true [(.generate-item item-generator "sword")]]))
      [])))
