;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2013 Tuukka Turto
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

(import [pyherc.test.builders [LevelBuilder CharacterBuilder]]
	[pyherc.ai.rat [is-next-to-wall? get-random-wall-direction RatAI]]
	[pyherc.ai.rat [map-direction]]
	[hamcrest [assert-that is- is-not :as is-not- none has-items is-in]]
	[hamcrest [equal-to]]
	[random [Random]])

(defn test-empty-space-is-detected [] 
  "test that an empty space is not reported as wall"
  (let [[level (-> (LevelBuilder)
                   (.with-floor-tile :floor)
		   (.with-wall-tile :empty-wall)
		   (.with-empty-wall-tile :empty-wall)
		   (.with-solid-wall-tile :solid-wall)
		   (.build))]]
    (assert-that (is-next-to-wall? level 5 9) (is- (equal-to False)))))

(defn test-wall-is-detected [] 
  "test that a wall can be detected next to a given point"
  (let [[level (-> (LevelBuilder)
                   (.with-floor-tile :floor)
		   (.with-wall-tile :empty-wall)
		   (.with-empty-wall-tile :empty-wall)
		   (.with-solid-wall-tile :solid-wall)
		   (.with-wall-at (, 4 10))
		   (.with-wall-at (, 5 10))
		   (.with-wall-at (, 6 10))
		   (.build))]]
    (assert-that (is-next-to-wall? level 5 9) (is- (equal-to True)))))

(defn test-mapping-directions []
  "test that keyword directions can be mapped to integers and back"
  (assert-that (map-direction :north) (is- (equal-to 1)))
  (assert-that (map-direction :south-west) (is- (equal-to 6)))
  (assert-that (map-direction 3) (is- (equal-to :east)))
  (assert-that (map-direction 9) (is- (equal-to :enter))))
