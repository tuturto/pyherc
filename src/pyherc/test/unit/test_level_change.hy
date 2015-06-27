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

(import [hamcrest [assert-that is- equal-to has-item]]) 
(import [pyherc.test.builders [CharacterBuilder]])
(import [pyherc.data [add-visited-level]]
        [pyherc.data.new-character [visited-levels↜]])

(defn test-add-visited-level []
  "test that adding and retrieving a level in visited list is possible"
  (let [[character (-> (CharacterBuilder)
                       (.build))]]
    (add-visited-level character "crystal forest")
    (assert-that (visited-levels↜ character)
                 (has-item "crystal forest"))))

(defn test-same-level-added-only-once []
  "test that same level can be added only once"
  (let [[character (-> (CharacterBuilder)
                       (.build))]]
    (add-visited-level character "crystal forest")
    (add-visited-level character "crystal forest")
    (assert-that (len (list (visited-levels↜ character)))
                 (is- (equal-to 1)))))
