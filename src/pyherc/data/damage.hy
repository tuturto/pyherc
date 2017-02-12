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

(require [hy.extra.anaphoric [ap-reduce]])
(require [pyherc.macros [*]])

(defn new-damage [damage-list]
  "create new damage function from a list of damage (amount, type)"
  (fn [target &optional [body-part "torso"]]
    "apply this damage to target's body-part, returns amount of damage done"
    (let [caused-damage (total-damage damage-list target body-part)]
      (setv target.hit-points (- target.hit-points (first caused-damage)))
      caused-damage)))

(defn total-damage [damage-list target body-part]
  "calculate total damage"
  (ap-reduce (sum-damage (apply-armour-bonus (modified-damage it target)
                                             target
                                             body-part) acc)
             damage-list #t(0 [])))

(defn sum-damage [damage total]
  "#t(total, [#t(damage type)]) + #t(damage type)"
  (.append (second total) damage)
  #t((+ (first total) (first damage))
     (second total)))

(defn modified-damage [damage target]
  "get damage modified by modifiers: #t(damage type)"
  (let [#t(damage-amount damage-type) damage
        total-modifiers (ap-reduce (+ it.modifier acc)
                                   (matching-modifiers↜ target damage-type)
                                   0)
        caused-damage (+ damage-amount total-modifiers)]
    (if (< caused-damage 1)
      #t(0 damage-type)
      #t(caused-damage damage-type))))

(defn matching-modifiers↜ [target damage-type]
  "return stream of matching damage modifiers"
  (genexpr x [x (.get-effects target)]
           (and (= x.effect-name "damage modifier")
                (= x.damage-type damage-type))))

(defn matching-modifiers [target damage-type]
  "return list of matching damage modifier"
  (list (matching-modifiers↜ target damage-type)))

(defn apply-armour-bonus [damage target body-part]
  "apply armour bonus to damage"
  (let [#t(damage-amount damage-type) damage
        reduction (armour-bonus target body-part)]
    (if (< reduction damage-amount) #t((- damage-amount reduction) damage-type)
        (< reduction (* 2 damage-amount)) #t(1 damage-type)
        #t(0 damage-type))))

(defn armour-bonus [target body-part]
  "get armour bonus for given body-part"
  (if (= body-part "feet") (if (is target.inventory.boots None)
                             0
                             target.inventory.boots.boots-data.damage-reduction)
      (if (is target.inventory.armour None)
        0
        target.inventory.armour.armour-data.damage-reduction)))
