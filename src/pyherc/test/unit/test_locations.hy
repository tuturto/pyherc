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

(import [pyherc.test.builders [LevelBuilder]]
        [pyherc.data [wall-tile next-to-wall?]]
        [hamcrest [assert-that is- equal-to]])
(require pyherc.macros)

(defn setup []
  "setup test cases"
  (let [[level (-> (LevelBuilder)
                   (.with-size #t(10 10))
                   (.with-wall-tile nil)
                   (.with-floor-tile :floor)
                   (.build))]]
    {:level level}))

(defn test-detect-wall []
  "wall should be detected"
  (let [[context (setup)]
        [level (:level context)]]
    (wall-tile level #t(6 5) :wall)
    (assert-that (next-to-wall? level #t(6 6)) (is- (equal-to true)))))

(defn test-empty-space-is-not-wall []
  "empty space is not reported as next to wall"
  (let [[context (setup)]
        [level (:level context)]]
    (assert-that (next-to-wall? level #t(6 6)) (is- (equal-to nil)))))

(defn test-between-walls-is-not-next-to-wall []
  "area between two walls is not reported as next to wall"
  (let [[context (setup)]
        [level (:level context)]]
    (wall-tile level #t(6 5))
    (wall-tile level #t(6 7))
    (assert-that (next-to-wall? level #t(6 6)) (is- (equal-to nil)))))
