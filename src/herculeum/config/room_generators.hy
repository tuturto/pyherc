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

(defn no-characters []
  "create character selector for nothing"
  (fn []
    []))

(defn skeletons [empty-pct character-generator rng]
  "create character selector for skeletons"
  (fn []
    (if (> (.randint rng 1 100) empty-pct)
      (let [roll (.randint rng 1 100)]
        (cond
         [True [(character-generator "skeleton warrior")]]))
      [])))

(defn no-items []
  "create item selector for nothing"
  (fn []
    []))

(defn altar-items [empty-pct item-generator rng]
  "create item selector for items found on common altars"
  (fn []
    (if (> (.randint rng 1 100) empty-pct)
      (let [roll (.randint rng 1 100)]
        (cond
         [(> roll 50) [(.generate-item item-generator "robes")]]
         [True [(.generate-item item-generator None "tome")]]))
      [])))

(defn mundane-items [empty-pct item-generator rng]
  "create item selector for mundane items"
  (fn []
    (if (> (.randint rng 1 100) empty-pct)
      (let [roll (.randint rng 1 100)]
        (if
         (> roll 40) [(.generate-item item-generator "club")]
         (> roll 20) [(.generate-item item-generator "dagger")]
         (> roll 10) [(.generate-item item-generator "axe")]
         [(.generate-item item-generator "sword")]))
      [])))
