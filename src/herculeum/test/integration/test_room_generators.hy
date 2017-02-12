;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2017 Tuukka Turto
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

(require [pyherc.macros [*]])
(require [hy.extra.anaphoric [*]])
(require [pyherc.config.dsl.level [*]])

(level-config-dsl)

(import [mockito [mock]])
(import [pyherc.data [Model]]
        [pyherc.data.traps [PitTrap]]
        [pyherc.generators [get-trap-creator]]
        [pyherc.generators.level.partitioners [grid-partitioning]]
        [pyherc.test.builders [LevelBuilder]]
        [random [Random]])
(import [herculeum.config.levels]
        [herculeum.config [Configuration]]
        [herculeum.config.room-generators [mundane-items skeletons]])

(defmacro run-generator [generator]
  `(let [level (-> (LevelBuilder)
                   (.with-size #t(30 20))
                   (.build))
         rng (Random)
         partitioner (grid-partitioning #t(10 10) 2 1 rng)
         sections (partitioner level)
         trap-config {"pit" [PitTrap {}]}]
     (ap-each sections (~generator it (get-trap-creator trap-config)))))

(defn setup-test []
  "setup test case"
  (let [config (Configuration (Model)
                              herculeum.config.levels
                              (mock)
                              (mock))]
    (.initialise config)
    {:config config}))

(defn test-square-room []
  "test generating square room"
  (run-generator (square-room "floor" "floor")))

(defn test-circular-room []
  "test generating circular room"
  (run-generator (circular-room "floor" "floor")))

(defn test-circular-cache-room []
  "test generating circular cache room"
  (let [context (setup-test)
        config (:config context)
        item-generator config.item-generator
        creature-generator config.creature-generator]
    (run-generator (circular-cache-room "floor" "floor" ["cache-tile"] 
                                        (mundane-items 50
                                                       item-generator
                                                       rng)
                                        (skeletons 50
                                                   creature-generator 
                                                   rng)))))

(defn test-circular-graveyard []
  "test generating circular graveyard"
  (let [context (setup-test)
        config (:config context)
        item-generator config.item-generator
        creature-generator config.creature-generator]
    (run-generator (circular-graveyard "floor" "floor" ["cache-tile"] 
                                       (mundane-items 50 item-generator rng)
                                       (skeletons 50 creature-generator
                                                  rng)))))

(defn test-square-graveyard []
  "test generating square graveyard"
  (let [context (setup-test)
        config (:config context)
        item-generator config.item-generator
        creature-generator config.creature-generator]
    (run-generator (square-graveyard "floor" "floor" ["cache-tile"] 
                                     (mundane-items 50 item-generator rng)
                                     (skeletons 50 creature-generator rng)))))

(defn test-square-library []
  "test generating square library"
  (run-generator (square-library "floor" "floor" ["shelves"])))

(defn test-circular-library []
  "test generating circular library"
  (run-generator (circular-library "floor" "floor" ["shelves"])))

(defn test-square-pitroom []
  "test generating square pitroom"
  (run-generator (square-pitroom "floor" "floor" "pit")))

(defn test-circular-pitroom []
  "test generating circular pitroom"
  (run-generator (circular-pitroom "floor" "floor" "pit")))

(defn test-square-band-room []
  "test generating square room with 2 tilings"
  (run-generator (square-band-room "floor1" "floor2" "floor")))

(defn test-square-banded-library []
  "test generating library with 2 tilings"
  (run-generator (square-banded-library "floor" "floor" "floor" ["shelves"] )))

(defn test-circular-band-room []
  "test generating circular room with 2 tilings"
  (run-generator (circular-band-room "floor" "floor" "floor")))

(defn test-pillar-room []
  "test generating pillar rooms"
  (run-generator (pillar-room "floor" "floor" ["pillar"])))
