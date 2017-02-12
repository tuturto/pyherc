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

(require [hy.extra.anaphoric [ap-each ap-map]])
(require [pyherc.macros [*]])

(import [pyherc.data [blocks-movement distance-between area-around]]
        [pyherc.generators.level.partitioners [section-floor section-wall
                                               section-data section-connections
                                               section-to-map section-level]])

(defn add-rows []
  "create generator for pre-placing rows"
  (fn [section &optional [trap-generator None]]
    (let [even-tiles []
          odd-tiles []]
      (ap-each (section-data section "room-tiles")
               (when (free-around? section it)
                 (if (odd? (second it)) (.append odd-tiles it)
                     (.append even-tiles it))))
      (section-data section "even-rows" even-tiles)
      (section-data section "odd-rows" odd-tiles)
      (if (> (len even-tiles) (len odd-tiles))
        (section-data section "rows" even-tiles)
        (section-data section "rows" odd-tiles)))))

(defn add-columns []
  "create generator for pre-placing columns"
  (fn [section &optional [trap-generator None]]
    (let [even-tiles []
          odd-tiles []]
      (ap-each (section-data section "room-tiles")
               (when (free-around? section it)
                 (if (odd? (first it)) (.append odd-tiles it)
                     (.append even-tiles it))))
      (section-data section "even-columns" even-tiles)
      (section-data section "odd-columns" odd-tiles)
      (if (> (len even-tiles) (len odd-tiles))
        (section-data section "columns" even-tiles)
        (section-data section "columns" odd-tiles)))))

(defn mark-center-area []
  "create generator to mark center area of room"
  (fn [section &optional [trap-generator None]]
    (let [center-tiles []]
      (ap-each (section-data section "room-tiles")
               (when (free-around? section it)
                 (.append center-tiles it)))
      (section-data section "center-area" center-tiles))))

(defn free-around? [section location]
  "are tiles around given section location free?"
  (let [tiles (list (area-around (section-to-map section location)))
        level (section-level section)
        non-blocking (list (ap-map (not (blocks-movement level it)) tiles))]
    (ap-reduce (and it acc) (list non-blocking))))
