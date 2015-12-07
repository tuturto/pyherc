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

(import [pyherc.test.builders [LevelBuilder]]
        [pyherc.data [wall-tile next-to-wall? open-area? corridor?]]
        [hamcrest [assert-that is- equal-to]])
(require pyherc.macros)

(defn setup []
  "setup test cases"
  (let [[level (-> (LevelBuilder)
                   (.with-size #t(10 10))
                   (.with-wall-tile nil)
                   (.with-floor-tile "floor")
                   (.build))]]
    {:level level}))

(defn test-detect-wall []
  "wall should be detected"
  (let [[context (setup)]
        [level (:level context)]]
    (wall-tile level #t(6 5) "wall")
    (assert-that (next-to-wall? level #t(6 6)) (is- (equal-to true)))))

(defn test-blocked-is-not-wall []
  "blocked tile is not next to wall"
  (let [[context (setup)]
        [level (:level context)]]
    (wall-tile level #t(6 5) "wall")
    (wall-tile level #t(6 6) "wall")
    (assert-that (next-to-wall? level #t(6 6)) (is- (equal-to false)))))

(defn test-empty-space-is-not-wall []
  "empty space is not reported as next to wall"
  (let [[context (setup)]
        [level (:level context)]]
    (assert-that (next-to-wall? level #t(6 6)) (is- (equal-to false)))))

(defn test-between-walls-is-not-next-to-wall []
  "area between two walls is not reported as next to wall"
  (let [[context (setup)]
        [level (:level context)]]
    (wall-tile level #t(6 5))
    (wall-tile level #t(6 7))
    (assert-that (next-to-wall? level #t(6 6)) (is- (equal-to false)))))

(defn test-corner-is-reported-next-to-wall []
  "corner should be considered next to wall"
  (let [[context (setup)]
        [level (:level context)]]
    (wall-tile level #t(6 5) "wall")
    (wall-tile level #t(7 5) "wall")
    (wall-tile level #t(7 6) "wall")
    (assert-that (next-to-wall? level #t(6 6)) (is- (equal-to true)))))

(defn test-empty-space-is-recognized []
  "empty space is recognized as empty space"
  (let [[context (setup)]
        [level (:level context)]]
    (assert-that (open-area? level #t(5 5)) (is- (equal-to true)))))

(defn test-blocked-location-is-not-empty []
  "blocked location is not recognized as empty area"
  (let [[context (setup)]
        [level (:level context)]]
    (wall-tile level #t(6 6) "wall")
    (assert-that (open-area? level #t(6 6)) (is- (equal-to false)))))

(defn test-next-to-wall-is-not-open-space []
  "area next to wall is not open space"
  (let [[context (setup)]
        [level (:level context)]]
    (wall-tile level #t(6 6) "wall")
    (assert-that (open-area? level #t(6 7)) (is- (equal-to false)))))

(defn test-open-area-is-not-corridor []
  "open area is not recognized as corridor"
  (let [[context (setup)]
        [level (:level context)]]
    (assert-that (corridor? level #t(6 6)) (is- (equal-to false)))))

(defn test-next-to-wall-is-not-corridor []
  "area next to wall is not considered a corridor"
  (let [[context (setup)]
        [level (:level context)]]
    (wall-tile level #t(5 5) "wall")
    (assert-that (corridor? level #t(6 5)) (is- (equal-to false)))))

(defn test-corner-is-not-corridor []
  "corner is not recognized as corridor"
  (let [[context (setup)]
        [level (:level context)]]
    (wall-tile level #t(5 5) "wall")
    (wall-tile level #t(6 5) "wall")
    (wall-tile level #t(6 6) "wall")
    (assert-that (corridor? level #t(5 6)) (is- (equal-to false)))))

(defn test-corridor-is-detected []
  "area between two walls is corridor"
  (let [[context (setup)]
        [level (:level context)]]
    (wall-tile level #t(5 5) "wall")
    (wall-tile level #t(5 7) "wall")
    (assert-that (corridor? level #t(5 6)) (is- (equal-to true)))))
