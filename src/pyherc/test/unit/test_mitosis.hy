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

(require [hy.extra.anaphoric [ap-each ap-dotimes]])
(require [pyherc.macros [*]])
(import [pyherc.test.builders [ActionFactoryBuilder CharacterBuilder
                               LevelBuilder MitosisFactoryBuilder]]
        [pyherc.data [Model add-character get-characters add-trap]]
        [pyherc.data.geometry [distance-between area-around]]
        [pyherc.data.traps [PitTrap]]
        [pyherc.ports [perform-mitosis mitosis-legal? set-action-factory]]
        [pyherc.generators [generate-creature creature-config]]
        [hamcrest [assert-that is- equal-to less-than greater-than-or-equal-to
                   all-of]]
        [functools [partial]]
        [random [Random]])

(defn setup []
  (let [model (Model)
        config {"fungi" (creature-config "fungi" 7 2 1 12 2 None 2)}
        generator (partial generate-creature
                           config
                           model
                           None
                           (Random))
        level (-> (LevelBuilder)
                  (.with-floor-tile "floor")
                  (.with-wall-tile None)
                  (.build))
        character (generator "fungi")
        action-factory (-> (ActionFactoryBuilder)
                           (.with-mitosis-factory
                            (-> (MitosisFactoryBuilder)
                                (.with-character-generator generator)
                                (.with-character-limit 10)
                                (.build)))
                           (.build))]
    (add-character level #t(5 5) character)
    (set-action-factory action-factory)
    {:model model
     :config config
     :generator generator
     :level level
     :character character}))

(defn test-character-can-duplicate []
  (let [context (setup)
        level (:level context)
        character (:character context)]
    (perform-mitosis character)
    (assert-that (count (get-characters level)) (is- (equal-to 2)))))

(defn test-new-character-is-generated-next-to-old-one []
  (let [context (setup)
        level (:level context)
        character (:character context)]
    (perform-mitosis character)
    (let [character₀ (first (list (get-characters level)))
          character₁ (second (list (get-characters level)))
          distance (distance-between character₀ character₁)]
      (assert-that distance (is- (less-than 2)))
      (assert-that distance (is- (greater-than-or-equal-to 1))))))

(defn test-new-character-is-not-generated-on-top-of-old-ones []
  (let [context (setup)
        level (:level context)
        character (:character context)        
        generator (:generator context)
        surrounding-tiles (area-around character.location)]
    (ap-each surrounding-tiles (let [new-character (generator "fungi")]
                                 (add-character level it new-character)))
    (perform-mitosis character)
    (assert-that (count (get-characters level)) (is- (equal-to 9)))))

(defn test-character-limit-is-observed []
  (let [context (setup)
        level (:level context)
        character (:character context)        
        generator (:generator context)
        surrounding-tiles (area-around character.location)]
    (ap-dotimes 9 (add-character level #t(it 2) (generator "fungi")))
    (assert-that (mitosis-legal? character) (is- (equal-to False)))))

(defn test-mitosis-triggers-traps []
  (let [context (setup)
        level (:level context)
        character (:character context)
        generator (:generator context)
        surrounding-tiles (area-around character.location)]
    (ap-each surrounding-tiles (add-trap level it (PitTrap)))
    (perform-mitosis character)
    (assert-that (count (get-characters level)) (is- (equal-to 1)))))
