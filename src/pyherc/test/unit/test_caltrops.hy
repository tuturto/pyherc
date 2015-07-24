;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2015 Tuukka Turto
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

(import [pyherc.data [add-trap get-traps]]
        [pyherc.data.traps [Caltrops]]
        [pyherc.test.builders [LevelBuilder]]
        [hamcrest [assert-that has-length]])

(defn test-placing-multiple-caltrops []
  "placing multiple caltrops is not possible"
  (let [[level (-> (LevelBuilder)
                   (.build))]]
    (add-trap level #t(5 5) (Caltrops 5))
    (add-trap level #t(5 5) (Caltrops 5))
    (assert-that (get-traps level #t(5 5)) (has-length 1))))
