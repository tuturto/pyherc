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

(import [hamcrest [assert-that contains-inanyorder is- equal-to]]
        [pyherc.generators.level [new-dungeon new-level add-level
                                  room-generators level-partitioners
                                  decorators items characters portals
                                  merge-level]])

(defn setup-context []
  "setup test dungeon configuration"
  (let [[dungeon (new-dungeon)]
        [level₀ (new-level "level₀"
                           ["room₀" "room₁"]
                           ["partitioner₀"]
                           ["decorator₀" "decorator₁"]
                           ["item₀"]
                           ["character₀" "character₁"]
                           ["portal₀"]
                           "test level")]
        [level₁ (new-level "level₁"
                           ["room₁" "room₂"]
                           ["partitioner₁"]
                           ["decorator₂" "decorator₃"]
                           ["item₁"]
                           ["character₁" "character₂"]
                           ["portal₁"]
                           "test level")]]
    (add-level dungeon level₀)
    (add-level dungeon level₁)
    {:dungeon dungeon
     :level₀ level₀
     :level₁ level₁}))

(defn test-room-config []
  "test that room configuration can be retrieved"
  (let [[context (setup-context)]
        [dungeon (:dungeon context)]]
    (assert-that (room-generators dungeon "level₀")
                 (contains-inanyorder "room₀" "room₁"))
    (assert-that (room-generators dungeon "level₁")
                 (contains-inanyorder "room₁" "room₂"))))

(defn test-partitioners []
  "test that partitioners can be retrieved"
  (let [[context (setup-context)]
        [dungeon (:dungeon context)]]
    (assert-that (level-partitioners dungeon "level₀")
                 (contains-inanyorder "partitioner₀"))
    (assert-that (level-partitioners dungeon "level₁")
                 (contains-inanyorder "partitioner₁"))))

(defn test-decorators []
  "test that decorators can be retrieved"
  (let [[context (setup-context)]
        [dungeon (:dungeon context)]]
    (assert-that (decorators dungeon "level₀")
                 (contains-inanyorder "decorator₀" "decorator₁"))
    (assert-that (decorators dungeon "level₁")
                 (contains-inanyorder "decorator₂" "decorator₃"))))

(defn test-items []
  "test that items can be retrieved"
  (let [[context (setup-context)]
        [dungeon (:dungeon context)]]
    (assert-that (items dungeon "level₀")
                 (contains-inanyorder "item₀"))
    (assert-that (items dungeon "level₁")
                 (contains-inanyorder "item₁"))))

(defn test-characters []
  "test that characters can be retrieved"
  (let [[context (setup-context)]
        [dungeon (:dungeon context)]]
    (assert-that (characters dungeon "level₀")
                 (contains-inanyorder "character₀" "character₁"))
    (assert-that (characters dungeon "level₁")
                 (contains-inanyorder "character₁" "character₂"))))

(defn test-portals []
  "test that portals can be retrieved"
  (let [[context (setup-context)]
        [dungeon (:dungeon context)]]
    (assert-that (portals dungeon "level₀")
                 (contains-inanyorder "portal₀"))
    (assert-that (portals dungeon "level₁")
                 (contains-inanyorder "portal₁"))))

(defn setup-merging-context []
  "setup testing context for merging tests"
  (let [[dungeon (new-dungeon)]
        [part₀ (new-level "level"
                          ["room₀" "room₁"]
                          ["partitioner₀"]
                          []
                          []
                          ["character₀" "character₁"]
                          ["portal₀"]
                          "test level")]
        [part₁ (new-level "level"
                          ["room₂" "room₃"]
                          []
                          ["decorator₂" "decorator₃"]
                          []
                          ["character₂" "character₃"]
                          ["portal₁"]
                          "test level")]
        [part₃ (new-level "another level"
                          ["room"]
                          ["partitioner"]
                          ["decorator"]
                          ["item"]
                          ["character"]
                          ["portal"]
                          "test level")]]
    (add-level dungeon part₀)
    {:dungeon dungeon
     :part₀ part₀
     :part₁ part₁
     :part₃ part₃}))

(defn test-merging-two-lists []
  "test that two lists can be merged"
  (let [[context (setup-merging-context)]
        [dungeon (:dungeon context)]
        [part₁ (:part₁ context)]]
    (merge-level dungeon part₁)
    (assert-that (room-generators dungeon "level")
                 (contains-inanyorder "room₀" "room₁" "room₂" "room₃"))))

(defn test-merging-empty []
  "test that merging into an empty list works"
  (let [[context (setup-merging-context)]
        [dungeon (:dungeon context)]
        [part₁ (:part₁ context)]]
    (merge-level dungeon part₁)
    (assert-that (level-partitioners dungeon "level")
                 (contains-inanyorder "partitioner₀"))))

(defn test-merging-into-empty []
  "test that merging into an empty list works"
  (let [[context (setup-merging-context)]
        [dungeon (:dungeon context)]
        [part₁ (:part₁ context)]]
    (merge-level dungeon part₁)
    (assert-that (decorators dungeon "level")
                 (contains-inanyorder "decorator₂" "decorator₃"))))

(defn test-merging-empty-lists []
  "test that merging two empty lists works"
  (let [[context (setup-merging-context)]
        [dungeon (:dungeon context)]
        [part₁ (:part₁ context)]]
    (merge-level dungeon part₁)
    (assert-that (len (list (items dungeon "level")))
                 (is- (equal-to 0)))))

(defn test-merging-completely-new-level []
  "test merging a completely new level into dungeon"
  (let [[context (setup-merging-context)]
        [dungeon (:dungeon context)]
        [another-level (:part₃ context)]]
    (merge-level dungeon another-level)
    (assert-that (room-generators dungeon "another level")
                 (contains-inanyorder "room"))))
