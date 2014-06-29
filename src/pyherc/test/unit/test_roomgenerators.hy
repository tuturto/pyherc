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

(require pyherc.macros)
(require hy.contrib.anaphoric)
(import [pyherc.data.traps [PitTrap]]
        [pyherc.generators.level.room [SquareRoomGenerator PillarRoomGenerator
                                       CacheRoomGenerator
                                       CatacombsGenerator CrimsonLairGenerator
                                       CircularRoomGenerator
                                       TempleRoomGenerator
                                       LibraryRoomGenerator
                                       PitRoomGenerator]]
        [pyherc.generators.level.partitioners [GridPartitioner]]
        [pyherc.test.builders [LevelBuilder]]
        [random [Random]])

(defn run-generator [generator]
  (let [[level (-> (LevelBuilder)
                   (.with-size #t(30 20))
                   (.build))]
        [partitioner (GridPartitioner ["test"] 2 1 (Random))]
        [sections (.partition-level partitioner level)]]
    (ap-each sections (.generate-room generator it))))

(defn test-catacombs-generator []
  "test generating catacombs"
  (run-generator (CatacombsGenerator :floor nil ["test"] (Random))))

(defn test-square-room-generator []
  "test generating square rooms"
  (run-generator (SquareRoomGenerator :floor nil :corridor ["test"])))

(defn test-pillar-room-generator []
  "test generating pillar rooms"
  (run-generator (PillarRoomGenerator :floor nil :corridor :pillar ["test"])))

(defn test-crimson-lair-generator []
  "test generating crimson lair"
  (run-generator (CrimsonLairGenerator :floor nil ["test"] (Random))))

(defn test-circular-room-generator []
  "test generating circular room"
  (run-generator (CircularRoomGenerator :floor :corridor ["test"])))

(defn test-temple-generation []
  "test generating temple"
  (run-generator (TempleRoomGenerator :floor :corridor :temple ["test"]
                                      :candle)))

(defn test-library-generation []
  "test generating library"
  (run-generator (LibraryRoomGenerator :floor :corridor [:shelf1 :shelf2] nil 50
                                       nil ["test"])))

(defn test-pitroom-generation []
  "test generating pit room"
  (run-generator (PitRoomGenerator :floor :corridor nil :pit PitTrap ["test"])))

(defn test-cacheroom-generation []
  "test generating cache room"
  (run-generator (CacheRoomGenerator :floor :corridor (fn [level center-point])
                                     ["test"])))
