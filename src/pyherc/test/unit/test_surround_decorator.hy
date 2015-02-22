;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2015 Tuukka Turto
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

(require pyherc.macros)
(import [pyherc.test.builders [LevelBuilder]]
        [pyherc.generators.level.decorator.wall [SurroundingDecorator
                                                 SurroundingDecoratorConfig]]
        [pyherc.data [wall-tile floor-tile]]
        [hamcrest [assert-that is- equal-to]])

(defn setup []
  "setup test cases"
  (let [[level (-> (LevelBuilder)
                   (.with-size #t(10 10))
                   (.with-floor-tile :floor)
                   (.with-wall-tile nil)
                   (.build))]
        [config (SurroundingDecoratorConfig [:any-level] :wall)]
        [decorator (SurroundingDecorator config)]]
    {:level level
     :decorator decorator}))

(defn test-surround-with-walls []
  "floor tiles next to null space should be walled in"
  (let [[context (setup)]
        [level (:level context)]
        [decorator (:decorator context)]]
    (.decorate-level decorator level)
    (assert-that (wall-tile level #t(0 -1)) (is- (equal-to :wall)))))


(defn test-floors-not-added []
  "no floors should be added while walling"
  (let [[context (setup)]
        [level (:level context)]
        [decorator (:decorator context)]]
    (.decorate-level decorator level)
    (assert-that (floor-tile level #t(0 -1)) (is- (equal-to nil)))))
