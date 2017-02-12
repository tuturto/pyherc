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

(import [pyherc.data [distance-between]]
        [pyherc.generators.level.partitioners [section-floor section-height
                                               section-width add-room-connection
                                               section-data section-connections
                                               connected-left connected-right
                                               connected-up connected-down]])

(defn circular-shape [floor-tile]
  "create a circular shape"
  (fn [section &optional [trap-generator None]]
    (assert floor-tile)
    (let [center-x (// (section-width section) 2)
          center-y (// (section-height section) 2)
          center-point #t(center-x center-y)
          radius (min [(- center-x 2) (- center-y 2)])
          room-tiles []]
      (for [x-loc (range (section-width section))]
        (for [y-loc (range (section-height section))]
          (when (<= (distance-between #t(x-loc y-loc) center-point) radius)
            (.append room-tiles #t(x-loc y-loc))
            (section-floor section #t(x-loc y-loc) floor-tile "room"))))
      (section-data section "room-tiles" room-tiles)
      (section-data section "center-point" center-point)
      (add-room-connection section #t(center-x (- center-y radius)) "up")
      (add-room-connection section #t(center-x (+ center-y radius)) "down")
      (add-room-connection section #t((- center-x radius) center-y) "left")
      (add-room-connection section #t((+ center-x radius) center-y) "right"))))

(defn square-shape [floor-tile rng]
  "create square shape"
  (assert floor-tile)
  (assert rng)
  (fn [section &optional [trap-generator None]]
    (let [middle-height (// (section-height section) 2)
          middle-width (// (section-width section) 2)
          room-left-edge (if (connected-left section)
                           (.randint rng 2 (- middle-width 2))
                           1)
          room-right-edge (if (connected-right section)
                            (.randint rng 
                                      (+ middle-width 2)
                                      (- (section-width section) 2))
                            (- (section-width section) 1))
          room-top-edge (if (connected-up section)
                          (.randint rng 2 (- middle-height 2))
                          1)
          room-bottom-edge (if (connected-down section)
                             (.randint rng 
                                       (+ middle-height 2)
                                       (- (section-height section) 2))
                             (- (section-height section) 1))
          center-x (+ (// (- room-right-edge room-left-edge) 2) room-left-edge)
          center-y (+ (// (- room-bottom-edge room-top-edge) 2) room-top-edge)
          room-tiles []]
      (for [loc-y (range (+ room-top-edge 1) room-bottom-edge)]
        (for [loc-x (range (+ room-left-edge 1) room-right-edge)]
          (.append room-tiles #t(loc-x loc-y))
          (section-floor section #t(loc-x loc-y) floor-tile "room")))
      (section-data section "room-tiles" room-tiles)
      (add-room-connection section #t(center-x room-top-edge) "up")
      (add-room-connection section #t(center-x room-bottom-edge) "down")
      (add-room-connection section #t(room-left-edge center-y) "left")
      (add-room-connection section #t(room-right-edge center-y) "right")
      (section-data section "corners" [#t((+ room-left-edge 1) (+ room-top-edge 1))
                                       #t((- room-right-edge 1) (+ room-top-edge 1))
                                       #t((- room-right-edge 1) (- room-bottom-edge 1))
                                       #t((+ room-left-edge 1) (- room-bottom-edge 1))])
      (section-data section "pillars" [#t((+ room-left-edge 2) (+ room-top-edge 2))
                                       #t((- room-right-edge 2) (+ room-top-edge 2))
                                       #t((- room-right-edge 2) (- room-bottom-edge 2))
                                       #t((+ room-left-edge 2) (- room-bottom-edge 2))]))))
