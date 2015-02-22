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

(import [pyherc.test.builders [CharacterBuilder]]
        [hamcrest [assert-that is- equal-to]]
        [pyherc.data [skill-ready?]])

(defn test-zero-cooldown []
  "a skill with zero cool down is ready to be used"
  (let [[character (-> (CharacterBuilder)
                       (.with-cooldown :shoryuken 0)
                       (.build))]]
    (assert-that (skill-ready? character :shoryuken)
                 (is- (equal-to true)))))

(defn test-non-zero-cooldown []
  "a skill with non-zero cool down is not ready to be used"
  (let [[character (-> (CharacterBuilder)
                       (.with-cooldown :shoryuken 200)
                       (.build))]]
    (assert-that (skill-ready? character :shoryuken)
                 (is- (equal-to false)))))
