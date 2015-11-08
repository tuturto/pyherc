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

(import [pyherc.solver [Variable are-equal! are-inequal! less-than!
                        solve solve-one value]]
        [hamcrest [assert-that is- equal-to is-not :as is-not- less-than]])

(defn context []
  "create an empty context for testing"
  {:frame-pointer 0
   :variable-stack []
   :value-stack []
   :solved false})

(defn test-simple-equality []
  "simple equality test"
  (let [[var₁ (Variable 1 2 3)]
        [var₂ (Variable 3 4 5)]]    
    (are-equal! var₁ var₂)
    (solve var₁ var₂)
    (assert-that (value var₁) (is- (equal-to (value var₂))))))

(defn test-simple-inequality []
  "inequal variables have different values"
  (let [[var₁ (Variable 1 2 3)]
        [var₂ (Variable 1 2 3)]]
    (are-inequal! var₁ var₂)
    (solve var₁ var₂)
    (assert-that (value var₁) (is-not- (equal-to (value var₂))))))

(defn test-less-than-constraint []
  "variable can be constrained to be less than something else"
  (let [[var₁ (Variable 1 2 3 4 5)]
        [var₂ (Variable 1 2 3 4 5)]]
    (less-than! var₁ var₂)
    (solve var₁ var₂)
    (assert-that (value var₁) (is- (less-than (value var₂))))))

(defn test-triple-less-than []
  "set of variables can be ordered with less-than!"
  (let [[var₁ (Variable 1 2 3 4 5)]
        [var₂ (Variable 1 2 3 4 5)]
        [var₃ (Variable 1 2 3 4 5)]]
    (less-than! var₁ var₂)
    (less-than! var₂ var₃)
    (solve var₁ var₂ var₃)
    (assert-that (value var₁) (is- (less-than (value var₂))))
    (assert-that (value var₂) (is- (less-than (value var₃))))))

(defn test-multiple-constraints []
  "variables with multiple constraints can be solved"
  (let [[var₁ (Variable 1 2 3 4 5)]
        [var₂ (Variable 1 2 3 4 5)]
        [var₃ (Variable 1 2 3 4 5)]]
    (are-equal! var₁ var₂)
    (are-inequal! var₁ var₃)
    (solve var₁ var₂ var₃)
    (assert-that (value var₁) (is- (equal-to (value var₂))))
    (assert-that (value var₁) (is-not- (equal-to (value var₃))))))

(defn test-single-value-left []
  "when variables have single value left, they are reported"
  (let [[var₁ (Variable 1)]
        [var₂ (Variable 2)]]
    (solve var₁ var₂)
    (assert-that (value var₁) (is- (equal-to 1)))
    (assert-that (value var₂) (is- (equal-to 2)))))
