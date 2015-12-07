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

(import [pyherc.solver [Variable are-equal! are-inequal! less-than!
                        greater-than! in-between! solve solve-one value]]
        [hamcrest [assert-that is- equal-to is-not :as is-not- less-than
                   greater-than]])

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

(defn test-basic-greater-than []
  "variable can be constrained to be greater than something else"
  (let [[var₁ (Variable 1 2 3 4 5)]
        [var₂ (Variable 1 2 3 4 5)]]
    (greater-than! var₁ var₂)
    (solve var₁ var₂)
    (assert-that (value var₁) (is- (greater-than (value var₂))))))

(defn test-basic-in-between []
  "variable can be constrained to be in-between two variables"
  (let [[var₁ (Variable 1 2 3 4 5)]
        [var₂ (Variable 1 2 3 4 5)]
        [var₃ (Variable 1 2 3 4 5)]]
    (in-between! var₁ var₂ var₃)
    (solve var₁ var₂ var₃)
    (assert-that (value var₁) (is- (greater-than (value var₂))))
    (assert-that (value var₁) (is- (less-than (value var₃))))))

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
