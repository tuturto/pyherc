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
                                               section-data section-connections
                                               connected-left connected-right
                                               connected-up connected-down]])

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

(defn square-shape [floor-tile rng]
  "create square shape"
  (fn [section]
    (let [[middle-height (// (section-height section) 2)]
          [middle-width (// (section-width section) 2)]
          [room-left-edge (if (connected-left section)
                            (.randint rng 2 (- middle-width 2))
                            1)]
          [room-right-edge (if (connected-right section)
                             (.randint rng 
                                       (+ middle-width 2)
                                       (- (section-width section) 2))
                             (- (section-width section) 1))]
          [room-top-edge (if (connected-up section)
                           (.randint rng 2 (- middle-height 2))
                           1)]
          [room-bottom-edge (if (connected-down section)
                              (.randint rng 
                                        (+ middle-height 2)
                                        (- (section-height section) 2))
                              (- (section-height section) 1))]
          [center-x (+ (// (- room-right-edge room-left-edge) 2) room-left-edge)]
          [center-y (+ (// (- room-bottom-edge room-top-edge) 2) room-top-edge)]]
      (for [loc-y (range (+ room-top-edge 1) room-bottom-edge)]
        (for [loc-x (range (+ room-left-edge 1) room-right-edge)]
          (section-floor section #t(loc-x loc-y) floor-tile "room")))
      (add-room-connection section #t(center-x room-top-edge) "up")
      (add-room-connection section #t(center-x room-bottom-edge) "down")
      (add-room-connection section #t(room-left-edge center-y) "left")
      (add-room-connection section #t(room-right-edge center-y) "right")
      (section-data section :corners [#t((+ room-left-edge 1) (+ room-top-edge 1))
                                      #t((- room-right-edge 1) (+ room-top-edge 1))
                                      #t((- room-right-edge 1) (- room-bottom-edge 1))
                                      #t((+ room-left-edge 1) (- room-bottom-edge 1))]))))
