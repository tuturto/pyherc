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

(require pyherc.macros)

(import [random]
        [hamcrest [assert-that has-length]]
        [pyherc.generators.level.partitioners [binary-space-partitioning]]
        [pyherc.test.builders [LevelBuilder]]
        [pyherc.test.matchers [are-not-overlapping]])

(defn test-too-small-area-is-not-partitioned []
  "when section is too small, it should not be partitioned further"
  (let [[level-size #t(20 20)]
        [room-min-size #t(21 21)]
        [level (-> (LevelBuilder)
                   (.build))]
        [partitioner (binary-space-partitioning level-size
                                                room-min-size
                                                random)]
        [sections (partitioner level)]]
    (assert-that (list sections) (has-length 1))))
  
(defn test-partition-horizontally []
  "wide and low section should be partitioned horizontally"
  (let [[level-size #t(25 10)]
        [room-min-size #t(10 10)]
        [level (-> (LevelBuilder)
                   (.build))]
        [partitioner (binary-space-partitioning level-size
                                                room-min-size
                                                random)]
        [sections (list (partitioner level))]]
    (assert-that sections (has-length 2))
    (assert-that sections (are-not-overlapping))))

(defn test-partition-vertically []
  "high and and narrow section should be partitioned vertically"
  (let [[level-size #t(10 25)]
        [room-min-size #t(10 10)]
        [level (-> (LevelBuilder)
                   (.build))]
        [partitioner (binary-space-partitioning level-size
                                                room-min-size
                                                random)]
        [sections (list (partitioner level))]]
    (assert-that sections (has-length 2))
    (assert-that sections (are-not-overlapping))))

(defn test-partition-multiple []
  "large section should have partitions both directions"
  (let [[level-size #t(25 25)]
        [room-min-size #t(10 10)]
        [level (-> (LevelBuilder)
                   (.build))]
        [partitioner (binary-space-partitioning level-size
                                                room-min-size
                                                random)]
        [sections (list (partitioner level))]]
    (assert-that sections (has-length 4))
    (assert-that sections (are-not-overlapping))))
