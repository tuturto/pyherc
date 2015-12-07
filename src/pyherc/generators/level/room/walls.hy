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

(import [pyherc.generators.level.partitioners [section-floor
                                               section-wall
                                               section-ornamentation]])

(defn floor-creator [floor-tiles position-selector rng]
  "create floor creator"
  (fn [section &optional [trap-generator nil]]
    "fill given area randomly with floor"
    (ap-each (position-selector section)
             (section-floor section it (.choice rng floor-tiles) nil))))

(defn wall-creator [wall-tiles position-selector rng]
  "create wall creator"
  (fn [section &optional [trap-generator nil]]
    "fill given area randomly with walls"
    (ap-each (position-selector section)
             (section-wall section it (.choice rng wall-tiles) nil))))

(defn ornament-creator [ornament-tiles position-selector rate rng]
  "create ornament creator"
  (fn [section &optional [trap-generator nil]]
    "fill given area randomly with ornaments"
    (ap-each (position-selector section)       
             (when (<= (.randint rng 0 100) rate) 
               (section-ornamentation section it 
                                      (.choice rng ornament-tiles))))))
