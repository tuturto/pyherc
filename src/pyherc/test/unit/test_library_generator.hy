;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2015 Tuukka Turto
;; 
;; Permission is hereby granted, free of charge, to any person obtaining a copy
;; of this software and associated documentation files (the "Software"), to deal
;; in the Software without restriction, including without limitation the rights
;; to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
;; copies of the Software, and to permit persons to whom the Software is
;; furnished to do so, subject to the following conditions:
;; 
;; The above copyright notice and this permission notice shall be included in
;; all copies or substantial portions of the Software.
;; 
;; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
;; IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
;; FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
;; AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
;; LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
;; OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
;; THE SOFTWARE.

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
                                                            ["coin"]
                                                            ["skeleton"])))]
        [generator (LibraryRoomGenerator "floor" "corridor" nil "grave" 100
                                         feature-creator ["test"])]]
    (ap-each sections (.generate-room generator it))
    (let [[grave (first (list (find-feature level)))]]
      (assert-that (items-in-cache grave) (has-item "coin"))
      (assert-that (characters-in-cache grave) (has-item "skeleton")))))
