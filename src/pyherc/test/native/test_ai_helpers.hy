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
	[pyherc.ai.rat [next-to-wall? get-random-wall-direction RatAI]]
	[pyherc.ai.rat [map-coordinates map-direction]]
	[hamcrest [assert-that is- is-not :as is-not- none has-items is-in]]
	[hamcrest [equal-to]]
	[random [Random]])

(defn test-empty-space-is-detected [] 
  "test that an empty space is not reported as wall"
  (let [[character (-> (CharacterBuilder)
		       (.build))]
	[ai (RatAI character)]
	[level (-> (LevelBuilder)
                   (.with-floor-tile :floor)
		   (.with-wall-tile :empty-wall)
		   (.with-empty-wall-tile :empty-wall)
		   (.with-solid-wall-tile :solid-wall)
		   (.with-character character (, 5 9))
		   (.build))]
	[wall-info (next-to-wall? ai)]]
    (assert-that wall-info (is- (none)))))

(defn test-wall-is-detected [] 
  "test that a wall can be detected next to a given point"
  (let [[character (-> (CharacterBuilder)
		       (.build))]
	[ai (RatAI character)]
	[level (-> (LevelBuilder)
                   (.with-floor-tile :floor)
		   (.with-wall-tile :empty-wall)
		   (.with-empty-wall-tile :empty-wall)
		   (.with-solid-wall-tile :solid-wall)
		   (.with-wall-at (, 4 10))
		   (.with-wall-at (, 5 10))
		   (.with-wall-at (, 6 10))
		   (.with-character character (, 5 9))
		   (.build))]
	[wall-info (next-to-wall? ai)]]
    (assert-that wall-info (is-not- (none)))
    (let [[wall-direction (:wall-direction wall-info)]]
      (assert-that wall-direction (has-items :east :west)))))

(defn test-picking-wall-direction-in-lip []
  "test that wall direction can be picked when a corridor is about to end"
  (let [[character (-> (CharacterBuilder)
		       (.build))]
	[ai (RatAI character)]
	[level (-> (LevelBuilder)
                   (.with-floor-tile :floor)
		   (.with-wall-tile :empty-wall)
		   (.with-empty-wall-tile :empty-wall)
		   (.with-solid-wall-tile :solid-wall)
		   (.with-wall-at (, 3 2))
		   (.with-wall-at (, 1 3))
		   (.with-wall-at (, 3 3))
		   (.with-character character (, 2 2))
		   (.build))]
	[wall-info (next-to-wall? ai)]]
    (assert-that wall-info (is-not- (none)))
    (let [[wall-direction (:wall-direction wall-info)]]
      (assert-that wall-direction (has-items :south)))))

(defn test-mapping-coordinates []
  "test that coordinates can be offset correctly"
  (let [[offset-1 (, -1 -1)]
	[offset-2 (, 2 4)]]
    (assert-that (map-coordinates (, 10 10) offset-1) (is- (equal-to (, 9 9))))
    (assert-that (map-coordinates (, 10 10) offset-2) (is- (equal-to (, 12 14))))))

(defn test-mapping-directions []
  "test that keyword directions can be mapped to integers and back"
  (assert-that (map-direction :north) (is- (equal-to 1)))
  (assert-that (map-direction :south-west) (is- (equal-to 6)))
  (assert-that (map-direction 3) (is- (equal-to :east)))
  (assert-that (map-direction 9) (is- (equal-to :enter))))
