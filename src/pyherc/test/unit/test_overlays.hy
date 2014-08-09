;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2014 Tuukka Turto
;;
;;  This file is part of pyherc.
;;
;;  pyherc is free software: you can redistribute it and/or modify
;;  it under the terms of the GNU General Public License as published by
;;  the Free Software Foundation, either version 3 of the License, or
;;  (at your option) any later version.
;;
;;  pyherc is distributed in the hope that it will be useful,
;;  but WITHOUT ANY WARRANTY; without even the implied warranty of
;;  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;  GNU General Public License for more details.
;;
;;  You should have received a copy of the GNU General Public License
;;  along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

(require hy.contrib.anaphoric)
(require pyherc.macros)

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
  (let [[level (-> (LevelBuilder)
                   (.with-size #t(10 10))
                   (.with-floor-tile nil)
                   (.with-wall-tile nil)
                   (.build))]
        [section (new-section #t(0 0) #t(9 9) level random)]
        [room-tiles []]]
    (for [loc-x (range 2 6)]
      (for [loc-y (range 2 6)]
        (section-floor section #t(loc-x loc-y) :floor)
        (.append room-tiles #t(loc-x loc-y))))
    (section-data section :room-tiles room-tiles)
    {:level level
     :section section}))

(defn test-creating-columns []
  "columns should be created in open space"
  (let [[context (setup)]
        [level (:level context)]
        [section (:section context)]]
    ((add-columns) section)
    (assert-that (section-data section :columns) (isnot (has-item #t(3 5))))
    (assert-that (section-data section :columns) (isnot (has-item #t(4 5))))
    (assert-that (section-data section :columns) (isnot (has-item #t(5 5))))))

(defn test-free-around []
  "free around should report if area is free around given location"
  (let [[context (setup)]
        [level (:level context)]
        [section (:section context)]]
    ((add-columns) section)
    (assert-that (free-around? section #t(3 4)) (is- (equal-to true)))
    (assert-that (free-around? section #t(3 5)) (is- (equal-to false)))))

(defn test-blocks-movement []
  "test that blocks movement works as expected"
  (let [[context (setup)]
        [level (:level context)]]
    (assert-that (blocks-movement level #t(3 5)) (is- (equal-to false)))
    (assert-that (blocks-movement level #t(3 6)) (is- (equal-to true)))))
