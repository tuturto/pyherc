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
        [hamcrest [assert-that has-item is-in is- equal-to]]
        [hamcrest [is-not :as isnot]]
        [pyherc.data [floor-tile blocks-movement wall-tile get-tile]]
        [pyherc.generators.level.partitioners [new-section section-data
                                               section-floor]]
        [pyherc.generators.level.room [add-columns]]
        [pyherc.generators.level.room.overlays [free-around?]]
        [pyherc.test.builders [LevelBuilder]])

(defn setup []
  "setup test cases"
  (let [level (-> (LevelBuilder)
                  (.with-size #t(10 10))
                  (.with-floor-tile None)
                  (.with-wall-tile None)
                  (.build))
        section (new-section #t(0 0) #t(9 9) level random)
        room-tiles []]
    (for [loc-x (range 2 6)]
      (for [loc-y (range 2 6)]
        (section-floor section #t(loc-x loc-y) "floor")
        (.append room-tiles #t(loc-x loc-y))))
    (section-data section "room-tiles" room-tiles)
    {:level level
     :section section}))

(defn test-creating-columns []
  "columns should be created in open space"
  (let [context (setup)
        level (:level context)
        section (:section context)]
    ((add-columns) section)
    (assert-that (section-data section "columns") (isnot (has-item #t(3 5))))
    (assert-that (section-data section "columns") (isnot (has-item #t(4 5))))
    (assert-that (section-data section "columns") (isnot (has-item #t(5 5))))))

(defn test-free-around []
  "free around should report if area is free around given location"
  (let [context (setup)
        level (:level context)
        section (:section context)]
    ((add-columns) section)
    (assert-that (free-around? section #t(3 4)) (is- (equal-to True)))
    (assert-that (free-around? section #t(3 5)) (is- (equal-to False)))))

(defn test-blocks-movement []
  "test that blocks movement works as expected"
  (let [context (setup)
        level (:level context)]
    (assert-that (blocks-movement level #t(3 5)) (is- (equal-to False)))
    (assert-that (blocks-movement level #t(3 6)) (is- (equal-to True)))))
