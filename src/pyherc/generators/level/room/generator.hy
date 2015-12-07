;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2015 Tuukka Turto
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
  (fn [section trap-generator]
    (ap-each creators (it section trap-generator))))

(defn tomes-and-potions-cache [item-generator]
  "create cache content creator"
  (fn []
    []))

(defn no-characters-cache [character-generator]
  "create cache character creator"
  (fn []
    []))

(defn fill-columns [tile]
  (fn [section trap-generator]
    (ap-each (section-data section "columns") (section-floor section it tile))))

(defn fill-rows [tile]
  (fn [section trap-generator]
    (ap-each (section-data section "rows") (section-floor section it tile))))
