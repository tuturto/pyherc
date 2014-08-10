;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2014 Tuukka Turto
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

(require pyherc.macros)

(import [random]
        [hamcrest [assert-that has-length]]
        [pyherc.generators.level.partitioners [binary-space-partitioning]]
        [pyherc.test.builders [LevelBuilder]])

(defn test-too-small-area-is-not-partitioned []
  "when section is too small, it should not be partitioned further"
  (let [[level-size #t(20 20)]
        [room-min-size #t(21 21)]
        [level (-> (LevelBuilder)
                   (.build))]
        [partitioner (binary-space-partitioning level-size room-min-size random)]
        [sections (partitioner level)]]
    (assert-that sections (has-length 1))))
  
;; (defn binary-space-partitioning [level-size room-min-size rng]
