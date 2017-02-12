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

(require [pyherc.macros [*]])
(require [hy.extra.anaphoric [ap-each]])

(import [pyherc.data [distance-between]]
        [pyherc.generators.level.room.corridor [CorridorGenerator]]
        [pyherc.generators.level.partitioners [section-width section-height
                                               section-floor
                                               section-ornamentation
                                               section-connections
                                               add-room-connection
                                               match-section-to-room]])

(defclass CircularRoomGenerator []
  "generator for circular rooms"
  [--init-- (fn [self floor-tile corridor-tile level-types]
              "default constructor"
              (setv self.center-point None)
              (setv self.floor-tile floor-tile)
              (setv self.corridor-tile corridor-tile)
              (setv self.level-types level-types))
   generate-room (fn [self section]
                   "generate a new room"
                   (let [center-x (// (section-width section) 2)
                         center-y (// (section-height section) 2)
                         center-point #t(center-x center-y)
                         radius (min [(- center-x 2) (- center-y 2)])]
                     (for [x_loc (range (section-width section))]
                       (for [y_loc (range (section-height section))]
                         (when (<= (distance-between #t(x_loc y_loc) center-point) radius)
                           (section-floor section #t(x_loc y_loc) self.floor-tile "room"))))
                     (add-room-connection section #t(center-x (- center-y radius)) "up")
                     (add-room-connection section #t(center-x (+ center-y radius)) "down")
                     (add-room-connection section #t((- center-x radius) center-y) "left")
                     (add-room-connection section #t((+ center-x radius) center-y) "right")
                     (.add-corridors self section)
                     (setv self.center-point center-point)))
   add-corridors (fn [self section]
                   "add corridors"
                   (ap-each (section-connections section)
                            (let [room-connection (match-section-to-room section it)
                                  corridor (CorridorGenerator room-connection
                                                              (.translate-to-section it)
                                                              None
                                                              self.corridor-tile)]
                              (.generate corridor))))])

(defclass TempleRoomGenerator [CircularRoomGenerator]
  "generator for temple rooms"
  [--init-- (fn [self floor-tile corridor-tile temple-tile level-types &optional candle-tile]
              "default constructor"
              (-> (super) (.--init-- floor-tile corridor-tile level-types))
              (setv self.temple-tile temple-tile)
              (setv self.candle-tile candle-tile))
   generate-room (fn [self section]
                   "generate a new room"
                   (-> (super) (.generate-room section))
                   (let [#t(x-loc y-loc) self.center-point]
                     (section-ornamentation section #t(x-loc y-loc) self.temple-tile)
                     (when self.candle-tile
                       (section-ornamentation section #t((+ x-loc 1) y-loc) self.candle-tile)
                       (section-ornamentation section #t((- x-loc 1) y-loc) self.candle-tile))))])
