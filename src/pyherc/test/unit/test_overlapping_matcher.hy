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
        [hamcrest [assert-that has-items]]
        [pyherc.generators.level.partitioners [new-section]]
        [pyherc.test.builders [LevelBuilder]]
        [pyherc.test.matchers.sections [all-corners]])

(defn test-all-corners-reported []
  "a section has 4 different corners"
  (let [[level (-> (LevelBuilder) (.build))]
        [section (new-section #t(0 0) #t(10 10) level random)]
        [corners (all-corners section)]]
    (assert-that corners (has-items #t(0 0) #t(10 10) #t(0 10) #t(10 0)))))

