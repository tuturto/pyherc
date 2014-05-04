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
(import [pyherc.test.builders [CharacterBuilder LevelBuilder]]
	[pyherc.rules.mitosis.interface [perform-mitosis]]
	[hamcrest [assert-that is- equal-to]])

(defn test-character-can-duplicate []
  (let [[level (-> (LevelBuilder)
		   (.build))]
	[character (-> (CharacterBuilder)
		       (.build))]]
    (.add-creature level character #t(5 5))
    (perform-mitosis character)
    (assert-that (len level.creatures) (is- (equal-to 2)))))
