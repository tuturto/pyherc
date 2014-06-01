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
(require hy.contrib.anaphoric)

(import [pyherc.data [distance-between]]
        [pyherc.generators.level.room.corridor [CorridorGenerator]])

(defclass CircularRoomGenerator []
  "generator for circular rooms"
  [[--init-- (fn [self floor-tile corridor-tile level-types]
               "default constructor"
               (setv self.center-point nil)
               (setv self.floor-tile floor-tile)
               (setv self.corridor-tile corridor-tile)
               (setv self.level-types level-types)
               nil)]
   [generate-room (fn [self section]
                    "generate a new room"
                    (let [[center-x (// section.width 2)]
                          [center-y (// section.height 2)]
                          [center-point #t(center-x center-y)]
                          [radius (min [(- center-x 2) (- center-y 2)])]]
                      (for [x_loc (range section.width)]
                        (for [y_loc (range section.height)]
                          (when (<= (distance-between #t(x_loc y_loc) center-point) radius)
                            (.set-floor section #t(x_loc y_loc) self.floor-tile "room"))))
                      (.add-room-connection section #t(center-x (- center-y radius)) "up")
                      (.add-room-connection section #t(center-x (+ center-y radius)) "down")
                      (.add-room-connection section #t((- center-x radius) center-y) "left")
                      (.add-room-connection section #t((+ center-x radius) center-y) "right")
                      (.add-corridors self section)
                      (setv self.center-point center-point)))]
   [add-corridors (fn [self section]
                    "add corridors"
                    (ap-each section.connections
                             (let [[room-connection (.find-room-connection section it)]
                                   [corridor (CorridorGenerator room-connection
                                                                (.translate-to-section it)
                                                                nil
                                                                self.corridor-tile)]]
                               (.generate corridor))))]])
