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

(require [hy.extra.anaphoric [ap-each]])
(require [hy.macros [*]])

(import [pyherc.generators.level.partitioners [section-data]])

(defn center-tile [section]
  "select center tile of section"
  [(section-data section "center-point")])

(defn random-rows [percentage rng]
  "create selector for picking random row tiles"
  (fn [section]
    (ap-each (section-data section "rows")
             (when (<= (.randint rng 1 100) percentage)
               (yield it)))))

(defn random-columns [percentage rng]
  "create selector for picking random column tiles"
  (fn [section]
    (ap-each (section-data section "columns")
             (when (<= (.randint rng 1 100) percentage)
               (yield it)))))

(defn random-pillars [percentage rng]
  "create selector for picking random pillar tiles"
  (fn [section]
    (ap-each (section-data section "pillars")
             (when (<= (.randint rng 1 100) percentage)
               (yield it)))))

(defn center-area []
  "create selector for picking center area of room"
  (fn [section]
    (ap-each (section-data section "center-area")
             (yield it))))

(defn side-by-side [area]
  "create selector for picking tiles side by side"
  (fn [section]
    (ap-each (area section) 
             (do 
              (yield (, (+ (first it) 1) (second it)))
              (yield (, (- (first it) 1) (second it)))))))
