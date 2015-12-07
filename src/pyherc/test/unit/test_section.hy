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

(import random
        [hamcrest [assert-that contains-inanyorder equal-to has-items
                   has-length is- has-item is-not :as -is-not]]
        [pyherc.test.builders [LevelBuilder]]
        [pyherc.data [floor-tile wall-tile get-location-tags]]
        [pyherc.generators.level.partitioners.section [new-section]]
        [pyherc.generators.level.partitioners [section-width section-height
                                               left-edge top-edge
                                               section-floor section-wall
                                               section-connections
                                               room-connections
                                               mark-neighbours
                                               mark-all-neighbours
                                               neighbour-sections
                                               unconnected-neighbours?
                                               section-border common-border
                                               opposing-point
                                               add-room-connection
                                               match-section-to-room
                                               connect-sections
                                               adjacent-sections?]])


(defn setup-calculation []
  "setup context for calculation tests"
  (let [[level (-> (LevelBuilder)
                   (.build))]
        [rng random]
        [section (new-section #t(10 10) #t(20 25) level rng)]]
    {:level level
     :rng rng
     :section section}))

(defn test-left-edge []
  "left edge calculation"
  (let [[context (setup-calculation)]
        [section (:section context)]]
    (assert-that (left-edge section) (is- (equal-to 10)))))

(defn test-top-edge []
  "top edge calculation"
  (let [[context (setup-calculation)]
        [section (:section context)]]
    (assert-that (top-edge section) (is- (equal-to 10)))))

(defn test-width []
  "test that width can be calculated"
  (let [[context (setup-calculation)]
        [section (:section context)]]
    (assert-that (section-width section) (is- (equal-to 10)))))

(defn test-height []
  "test that height can be calculated correctly"
  (let [[context (setup-calculation)]
        [section (:section context)]]
    (assert-that (section-height section) (is- (equal-to 15)))))

(defn test-border []
  "test that section can report border"
  (let [[context (setup-calculation)]
        [section (:section context)]
        [border (list (section-border section))]]
    (assert-that border (has-items #t(11 10 "down") #t(12 10 "down")
                                   #t(18 10 "down") #t(19 10 "down")
                                   #t(10 11 "right") #t(10 12 "right")
                                   #t(10 23 "right") #t(10 24 "right")
                                   #t(11 25 "up") #t(12 25 "up")
                                   #t(18 25 "up") #t(19 25 "up")
                                   #t(20 11 "left") #t(20 12 "left")
                                   #t(20 23 "left") #t(20 24 "left")))))

(defn setup-section-connections []
  "setup sections with connections for testing"
  (let [[level (-> (LevelBuilder)
                   (.build))]
        [section₁ (new-section #t(0 0) #t(10 20) level random)]
        [section₂ (new-section #t(11 0) #t(20 20) level random)]]
    (mark-neighbours section₁ section₂)
    {:level level
     :section₁ section₁
     :section₂ section₂}))

(defn test-unconnected-neighbours []
  "test that unconnected neighbours can be detected"
  (let [[context (setup-section-connections)]
        [section (:section₁ context)]]
    (assert-that (unconnected-neighbours? section))))

(defn test-connected-neighbours-are-not-reported []
  "test that connected neighbours are not reported as unconnected"
  (let [[context (setup-section-connections)]
        [section₁ (:section₁ context)]
        [section₂ (:section₂ context)]]
    (connect-sections section₁ section₂)
    (assert-that (-is-not (unconnected-neighbours? section₁)))))

(defn test-section-connection-points []
  "test that linked sections have their connection points set up
   so that they line up in the border"
  (let [[context (setup-section-connections)]
        [section₁ (:section₁ context)]
        [section₂ (:section₂ context)]]
    (connect-sections section₁ section₂)
    (let [[point₁ (first (list (section-connections section₁)))]
          [point₂ (first (list (section-connections section₂)))]]
      (assert-that (first point₁.location) (is- (equal-to 10)))
      (assert-that (first point₂.location) (is- (equal-to 11)))
      (assert-that (second point₁.location)
                   (is- (equal-to (second point₂.location)))))))

(defn test-section-connections-have-direction []
  "test that connections between section have direction"
  (let [[context (setup-section-connections)]
        [section₁ (:section₁ context)]
        [section₂ (:section₂ context)]]
    (connect-sections section₁ section₂)
    (let [[point₁ (first (list (section-connections section₁)))]
          [point₂ (first (list (section-connections section₂)))]]
      (assert-that point₁.direction (is- (equal-to "left")))
      (assert-that point₂.direction (is- (equal-to "right"))))))

(defn test-common-border []
  "test that section can calculate common border with another section"
  (let [[context (setup-section-connections)]
        [section₁ (:section₁ context)]
        [section₂ (:section₂ context)]
        [border (list (common-border section₁ section₂))]]
    (assert-that border (contains-inanyorder #t(10 1 "left") #t(10 2 "left")
                                             #t(10 3 "left") #t(10 4 "left")
                                             #t(10 5 "left") #t(10 6 "left")
                                             #t(10 7 "left") #t(10 8 "left")
                                             #t(10 9 "left") #t(10 10 "left")
                                             #t(10 11 "left") #t(10 12 "left")
                                             #t(10 13 "left") #t(10 14 "left")
                                             #t(10 15 "left") #t(10 16 "left")
                                             #t(10 17 "left") #t(10 18 "left")
                                             #t(10 19 "left")))))

(defn test-get-opposing-point []
  "test that section can calculate which of its points corresponds to the
   point given on the other side of the border"
  (let [[context (setup-section-connections)]
        [section (:section₂ context)]
        [other-point (opposing-point section #t(10 9))]]
    (assert-that other-point (is- (equal-to #t(11 9 "right"))))))

(defn test-adding-room-connections []
  "test that added room connections are tracked"
  (let [[context (setup-section-connections)]
        [section (:section₁ context)]]
    (add-room-connection section #t(5 5) "right")
    (assert-that (list (room-connections section)) (has-length 1))))

(defn test-finding-room-connection []
  "test that room connection can be found for given section connection"
  (let [[context (setup-section-connections)]
        [section₁ (:section₁ context)]
        [section₂ (:section₂ context)]]
    (add-room-connection section₁ #t(7 5) "right")
    (add-room-connection section₁ #t(3 5) "left")
    (add-room-connection section₁ #t(5 7) "down")
    (add-room-connection section₁ #t(5 3) "down")
    (connect-sections section₁ section₂)
    (let [[edge-connection (first (list (section-connections section₁)))]
          [connection (match-section-to-room section₁ edge-connection)]]
      (assert-that connection.direction (is- (equal-to "right"))))))

(defn setup-level-access []
  "setup test for level access"
  (let [[rng random]
        [level (-> (LevelBuilder)
                   (.with-size #t(10 10))
                   (.with-floor-tile "floor-empty")
                   (.with-wall-tile "wall-empty")
                   (.build))]
        [section (new-section #t(0 0) #t(10 10) level rng)]]
    {:level level
     :section section}))

(defn test-setting-floor []
  "test that floor can be set"
  (let [[context (setup-level-access)]
        [section (:section context)]
        [level (:level context)]]
    (section-floor section #t(5 5) "floor-rock" nil)
    (assert-that (floor-tile level #t(5 5))
                 (is- (equal-to "floor-rock")))))

(defn test-setting-wall []
  "test that wall can be set"
  (let [[context (setup-level-access)]
        [section (:section context)]
        [level (:level context)]]
    (section-wall section #t(2 2) "wall-ground" nil)
    (assert-that (wall-tile level #t(2 2))
                 (is- (equal-to "wall-ground")))))

(defn test-setting-location-type []
  "test that location type can be set correctly"
  (let [[context (setup-level-access)]
        [section (:section context)]
        [level (:level context)]]
    (section-floor section #t(2 3) "floor-rock" "corridor")
    (assert-that (get-location-tags level #t(2 3)) (has-item "corridor"))))

(defn setup-level-access-with-offset []
  "setup test case for level access with offset"
  (let [[level (-> (LevelBuilder)
                   (.with-size #t(10 10))
                   (.with-floor-tile "floor-empty")
                   (.with-wall-tile "wall-empty")
                   (.build))]
        (section (new-section #t(5 5) #t(10 10) level random))]
    {:level level
     :section section}))

(defn test-setting-floor-with-offset []
  "test that offset section is correctly mapped to the level"
  (let [[context (setup-level-access-with-offset)]
        [level (:level context)]
        [section (:section context)]]
    (section-floor section #t(2 2) "floor-rock" nil)
    (assert-that (floor-tile level #t(7 7))
                 (is- (equal-to "floor-rock")))))

(defn test-setting-wall-with-offset []
  "test that offset section is correctly mapped to the level"
  (let [[context (setup-level-access-with-offset)]
        [level (:level context)]
        [section (:section context)]]
    (section-wall section #t(3 2) "wall-ground" nil)
    (assert-that (wall-tile level #t(8 7))
                 (is- (equal-to "wall-ground")))))

(defn test-marking-neighbours []
  "test that list of sections can be marked neighbours"
  (let [[level (-> (LevelBuilder)
                   (.build))]
        [section₀ (new-section #t(0 0) #t(10 15) level random)]
        [section₁ (new-section #t(11 0) #t(20 15) level random)]
        [section₂ (new-section #t(21 0) #t(30 15) level random)]]
    (mark-all-neighbours [section₀ section₁ section₂])
    (assert-that (neighbour-sections section₀)
                 (contains-inanyorder section₁))
    (assert-that (neighbour-sections section₁)
                 (contains-inanyorder section₀ section₂))
    (assert-that (neighbour-sections section₂)
                 (contains-inanyorder section₁))))

(defn test-adjacent-sections []
  "adjacent sections should be detected"
  (ylet [[level (-> (LevelBuilder)
                    (.build))]
         [section (new-section #t(10 10) #t(13 13) level random)]
         [check (fn [a b] (do
                           (assert-that (adjacent-sections? a b)
                                        (equal-to true))))]]
        (for [x (range 9 12)]
          (yield #t(check section (new-section #t(x 0)
                                               #t((+ x 3) 9)
                                               level
                                               random)))
          (yield #t(check section (new-section #t(x 14)
                                               #t((+ x 3) 18)
                                               level
                                               random))))
        (for [y (range 9 12)]
          (yield #t(check section (new-section #t(0 y)
                                               #t(9 (+ y 3))
                                               level
                                               random)))
          (yield #t(check section (new-section #t(14 y)
                                               #t(18 (+ y 3))
                                               level
                                               random))))))

(defn test-non-adjacent-sections []
  "non-adjacent sections should not be marked as adjacent"
  (ylet [[level (-> (LevelBuilder)
                    (.build))]
         [section (new-section #t(10 10) #t(13 13) level random)]
         [check (fn [a b] (assert-that (adjacent-sections? a b)
                                       (equal-to false)))]]
        (for [x (range 4 18)]
          (yield #t(check section (new-section #t(x 0)
                                               #t((+ x 3) 8)
                                               level
                                               random)))
          (yield #t(check section (new-section #t(x 15)
                                               #t((+ x 3) 18)
                                               level
                                               random))))
        (for [y (range 4 18)]
          (yield #t(check section (new-section #t(0 y)
                                               #t(8 (+ y 3))
                                               level
                                               random)))
          (yield #t(check section (new-section #t(15 y)
                                               #t(18 (+ y 3))
                                               level
                                               random))))))
