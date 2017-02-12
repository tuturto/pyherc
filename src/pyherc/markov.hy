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
(import [random [Random]])

(defn chain-factory [start-elements elements continue-fn]
  "create factory function that can create markov chain instances"
  (fn [&optional [seed None]]
    "create generator for chain"
    (setv rng (if seed
                (Random seed)
                (Random))) 
    (defn select-next-element [elements-list]
      "select element"
      (let [high (max (list-comp upper [#t (element lower upper) elements-list]))
            value (.randint rng 0 high)
            matches (list-comp element [#t (element lower upper) elements-list]
                               (> lower value upper))]
        (if matches
          (first (.choice rng matches))
          (first (.choice rng elements-list)))))

    (setv current-element (select-next-element start-elements))
    (setv running True)
    (yield current-element)
    (while running
      (setv next-elements (get elements current-element))
      (setv current-element (select-next-element next-elements))
      (setv running (continue-fn current-element))
      (when (not running) (break))
      (yield current-element))))
