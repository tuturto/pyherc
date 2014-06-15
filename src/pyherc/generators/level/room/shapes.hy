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

(require pyherc.macros)

(import [pyherc.data [distance-between]]
        [pyherc.generators.level.partitioners [section-floor section-height
                                               section-width add-room-connection
                                               section-data]])

(defn circular-shape [floor-tile]
  "create a circular shape"
  (fn [section]
    (let [[center-x (// (section-width section) 2)]
          [center-y (// (section-height section) 2)]
          [center-point #t(center-x center-y)]
          [radius (min [(- center-x 2) (- center-y 2)])]]
      (for [x_loc (range (section-width section))]
        (for [y_loc (range (section-height section))]
          (when (<= (distance-between #t(x_loc y_loc) center-point) radius)
            (section-floor section #t(x_loc y_loc) floor-tile "room"))))
      (section-data section :center-point center-point)
      (add-room-connection section #t(center-x (- center-y radius)) "up")
      (add-room-connection section #t(center-x (+ center-y radius)) "down")
      (add-room-connection section #t((- center-x radius) center-y) "left")
      (add-room-connection section #t((+ center-x radius) center-y) "right"))))
