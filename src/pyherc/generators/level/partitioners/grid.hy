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

(import [pyherc.generators.level.partitioners.section [new-section
                                                       mark-all-neighbours]])

(defn grid-partitioning [room-size horizontal-repeats vertical-repeats rng]
  "create a new partitioner"
  (fn [level]
    "partition a level"    
    (let [sections []
          #t(width height) room-size] 
      (for [x (range horizontal-repeats)]
        (for [y (range vertical-repeats)]
          (.append sections 
                   (new-section #t((* width x) (* height y)) 
                                #t((+ 1 (* width (+ x 1)))
                                   (+ 1 (* height (+ y 1)))) 
                                level 
                                rng))))
      (mark-all-neighbours sections)
      sections)))
