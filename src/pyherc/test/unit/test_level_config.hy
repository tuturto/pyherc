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
