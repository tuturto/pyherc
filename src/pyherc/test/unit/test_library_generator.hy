;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2014 Tuukka Turto
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

(require hy.contrib.anaphoric)
(require pyherc.macros)

(import [random [Random]])
(import [hamcrest [assert-that has-item]])
(import [pyherc.data [add-location-feature get-tiles location-features]]
        [pyherc.data.features [new-cache items-in-cache characters-in-cache]]
        [pyherc.generators.level.partitioners [grid-partitioning]]
        [pyherc.generators.level.room [LibraryRoomGenerator]]
        [pyherc.test.builders [LevelBuilder]])

(defn setup[]
  (let [[level (-> (LevelBuilder)
                   (.with-size #t(30 20))
                   (.build))]
        [partitioner (grid-partitioning #t(10 10) 2 1 (Random))]
        [sections (partitioner level)]]
    {:level level
     :sections sections}))

(defn find-feature [level]
  "find a grave"
  (for [#t(location tile) (get-tiles level)]
    (yield-from (location-features level location))))

(defn test-adding-special-feature[]
  "library generator can add special features"
  (let [[context (setup)]
        [level (:level context)]
        [sections (:sections context)]
        [feature-creator (fn [level location]
                           (add-location-feature level
                                                 location
                                                 (new-cache level
                                                            location
                                                            [:coin]
                                                            [:skeleton])))]
        [generator (LibraryRoomGenerator :floor :corridor nil :grave 100
                                         feature-creator ["test"])]]
    (ap-each sections (.generate-room generator it))
    (let [[grave (first (list (find-feature level)))]]
      (assert-that (items-in-cache grave) (has-item :coin))
      (assert-that (characters-in-cache grave) (has-item :skeleton)))))
