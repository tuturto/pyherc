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

(require pyherc.macros)
(require hy.contrib.anaphoric)
(import [pyherc.data.traps [PitTrap]]
        [pyherc.generators.level.room [SquareRoomGenerator PillarRoomGenerator
                                       CacheRoomGenerator
                                       CatacombsGenerator CrimsonLairGenerator
                                       CircularRoomGenerator
                                       TempleRoomGenerator
                                       LibraryRoomGenerator]]
        [pyherc.generators.level.partitioners [grid-partitioning]]
        [pyherc.test.builders [LevelBuilder]]
        [random [Random]])

(defn run-generator [generator]
  (let [[level (-> (LevelBuilder)
                   (.with-size #t(30 20))
                   (.build))]
        [partitioner (grid-partitioning #t(10 10) 2 1 (Random))]
        [sections (partitioner level)]]
    (ap-each sections (.generate-room generator it))))

(defn test-catacombs-generator []
  "test generating catacombs"
  (run-generator (CatacombsGenerator "floor" nil ["test"] (Random))))

(defn test-square-room-generator []
  "test generating square rooms"
  (run-generator (SquareRoomGenerator "floor" nil "corridor" ["test"])))

(defn test-pillar-room-generator []
  "test generating pillar rooms"
  (run-generator (PillarRoomGenerator "floor" nil "corridor" "pillar" ["test"])))

(defn test-crimson-lair-generator []
  "test generating crimson lair"
  (run-generator (CrimsonLairGenerator "floor" nil ["test"] (Random))))

(defn test-circular-room-generator []
  "test generating circular room"
  (run-generator (CircularRoomGenerator "floor" "corridor" ["test"])))

(defn test-temple-generation []
  "test generating temple"
  (run-generator (TempleRoomGenerator "floor" "corridor" "temple" ["test"]
                                      "candle")))

(defn test-library-generation []
  "test generating library"
  (run-generator (LibraryRoomGenerator "floor" "corridor" ["shelf1" "shelf2"] nil 50
                                       nil ["test"])))

(defn test-cacheroom-generation []
  "test generating cache room"
  (run-generator (CacheRoomGenerator "floor" "corridor" (fn [level center-point])
                                     ["test"])))
