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

(import [random]
        [hamcrest [assert-that has-items is- equal-to]]
        [pyherc.generators.level.partitioners [new-section]]
        [pyherc.test.builders [LevelBuilder]]
        [pyherc.test.matchers.sections [all-corners inside-square?
                                        overlapping?]])

(defn test-all-corners-reported []
  "a section has 4 different corners"
  (let [level (-> (LevelBuilder) (.build))
        section (new-section #t(0 0) #t(10 10) level random)
        corners (all-corners section)]
    (assert-that corners (has-items #t(0 0) #t(10 10) #t(0 10) #t(10 0)))))

(defn test-point-inside-square []
  "test that points inside of a square are detected correctly"
  (let [level (-> (LevelBuilder) (.build))
        section (new-section #t(0 0) #t(10 10) level random)]
    (assert-that (inside-square? #t(0 0) section) (is- (equal-to True)))
    (assert-that (inside-square? #t(10 10) section) (is- (equal-to True)))
    (assert-that (inside-square? #t(0 10) section) (is- (equal-to True)))
    (assert-that (inside-square? #t(10 0) section) (is- (equal-to True)))
    (assert-that (inside-square? #t(5 5) section) (is- (equal-to True)))))

(defn test-point-outside-square []
  "points outside of section should not reported being inside"
  (let [level (-> (LevelBuilder) (.build))
        section (new-section #t(0 0) #t(10 10) level random)]
    (assert-that (inside-square? #t(5 -5) section) (is- (equal-to False)))
    (assert-that (inside-square? #t(15 5) section) (is- (equal-to False)))
    (assert-that (inside-square? #t(5 15) section) (is- (equal-to False)))
    (assert-that (inside-square? #t(-5 5) section) (is- (equal-to False)))))

(defn test-overlapping-sections-are-detected []
  "two overlapping sections are detected"
  (let [level (-> (LevelBuilder) (.build))
        section₀ (new-section #t(0 0) #t(10 10) level random)
        section₁ (new-section #t(8 0) #t(20 10) level random)
        sections [section₀ section₁]]
    (assert-that (overlapping? section₀ sections) (is- (equal-to True)))))
