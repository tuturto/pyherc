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
(import [mockito [mock]])
(import [pyherc.data [Model]]
        [pyherc.generators.level.partitioners [grid-partitioning]]
        [pyherc.test.builders [LevelBuilder]]
        [random [Random]])
(import [herculeum.config.levels]
        [herculeum.config [Configuration]]
        [herculeum.config.room-generators [square-room circular-room
                                           circular-cache-room
                                           circular-graveyard square-graveyard
                                           square-library circular-library
                                           mundane-items skeletons]])

(defn run-generator [generator]
  (let [[level (-> (LevelBuilder)
                   (.with-size #t(30 20))
                   (.build))]
        [partitioner (grid-partitioning #t(10 10) 2 1 (Random))]
        [sections (partitioner level)]]
    (ap-each sections (generator it))))

(defn setup-test []
  "setup test case"
  (let [[config (Configuration (Model)
                               herculeum.config.levels
                               (mock)
                               (mock))]]
    (.initialise config)
    {:config config}))

(defn test-catacombs-generator []
  "test generating square room"
  (run-generator (square-room :floor :floor (Random))))

(defn test-circular-room []
  "test generating circular room"
  (run-generator (circular-room :floor :floor (Random))))

(defn test-circular-cache-room []
  "test generating circular cache room"
  (let [[context (setup-test)]
        [config (:config context)]
        [item-generator config.item-generator]
        [creature-generator config.creature-generator]
        [rng (Random)]]
    (run-generator (circular-cache-room :floor :floor [:cache-tile] 
                                        (mundane-items 50 item-generator rng)
                                        (skeletons 50 creature-generator rng)
                                        rng))))

(defn test-circular-graveyard []
  "test generating circular graveyard"
  (let [[context (setup-test)]
        [config (:config context)]
        [item-generator config.item-generator]
        [creature-generator config.creature-generator]
        [rng (Random)]]
    (run-generator (circular-graveyard :floor :floor [:cache-tile] 
                                       (mundane-items 50 item-generator rng)
                                       (skeletons 50 creature-generator rng)
                                       rng))))

(defn test-square-graveyard []
  "test generating square graveyard"
  (let [[context (setup-test)]
        [config (:config context)]
        [item-generator config.item-generator]
        [creature-generator config.creature-generator]
        [rng (Random)]]
    (run-generator (square-graveyard :floor :floor [:cache-tile] 
                                     (mundane-items 50 item-generator rng)
                                     (skeletons 50 creature-generator rng)
                                     rng))))

(defn test-square-library []
  "test generating square library"
  (run-generator (square-library :floor :floor [:shelves] (Random))))

(defn test-circular-library []
  "test generating circular library"
  (run-generator (circular-library :floor :floor [:shelves] (Random))))
