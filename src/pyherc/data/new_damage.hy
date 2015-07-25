;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2015 Tuukka Turto
;;
;;   This file is part of pyherc.
;;
;;   pyherc is free software: you can redistribute it and/or modify
;;   it under the terms of the GNU General Public License as published by
;;   the Free Software Foundation, either version 3 of the License, or
;;   (at your option) any later version.
;;
;;   pyherc is distributed in the hope that it will be useful,
;;   but WITHOUT ANY WARRANTY; without even the implied warranty of
;;   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;   GNU General Public License for more details.
;;
;;   You should have received a copy of the GNU General Public License
;;   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

(require hy.contrib.anaphoric)

(defn new-damage [damage-list]
  "create new damage function from a list of damage (amount, type)"
  (fn [target body-part]
    "apply this damage to target's body-part, returns amount of damage done"
    (let [[caused-damage (total-damage damage-list target body-part)]]
      (setv target.hit-points (- target.hit-points caused-damage))
      caused-damage)))

(defn total-damage [damage-list target body-part]
  "calculate total damage"
  (ap-reduce (+ (apply-armour-bonus (modified-damage it target)
                                    target
                                    body-part) acc)
             damage-list 0))

(defn modified-damage [damage target]
  "get damage modified by modifiers"
  (let [[damage-amount (first damage)]
        [damage-type (second damage)]
        [total-modifiers (ap-reduce (+ it.modifier acc)
                                    (matching-modifiers↜ target damage-type)
                                    0)]
        [caused-damage (+ damage-amount total-modifiers)]]
    (if (< caused-damage 1) 0 caused-damage)))

(defn matching-modifiers↜ [target damage-type]
  "return stream of matching damage modifiers"
  (genexpr x [x (.get-effects target)]
           (and (= x.effect-name "damage modifier")
                (= x.damage-type damage-type))))

(defn matching-modifiers [target damage-type]
  "return list of matching damage modifier"
  (list (matching-modifiers↜ target damage-type)))

(defn apply-armour-bonus [damage-amount target body-part]
  "apply armour bonus to damage"
  (let [[reduction (armour-bonus target body-part)]]
    (cond [(< reduction damage-amount) (- damage-amount reduction)]
          [(< reduction (* 2 damage-amount)) 1]
          [true 0])))

(defn armour-bonus [target body-part]
  "get armour bonus for given body-part"
  (cond [(= body-part "feet") (if (is target.inventory.boots nil)
                                0
                                target.inventory.boots.boots-data.damage-reduction)]
        [true (if (is target.inventory.armour nil)
                0
                target.inventory.armour.armour-data.damage-reduction)]))

