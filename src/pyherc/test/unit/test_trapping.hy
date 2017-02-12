;; -*- coding: utf-8 -*-

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

(import [pyherc.data [get-traps]]
        [pyherc.data.traps [Caltrops]]
        [pyherc.generators [get-trap-creator]]
        [pyherc.ports [place-trap place-natural-trap trapping-legal?
                       set-action-factory]]
        [pyherc.test.builders [ActionFactoryBuilder CharacterBuilder
                               LevelBuilder ItemBuilder
                               TrappingFactoryBuilder]]
        [hamcrest [assert-that has-length is- equal-to greater-than less-than
                   has-item]]
        [hamcrest [is-not :as is-not-]])

(defn setup []
  "setup test case"
  (let [trap-config {"caltrops" [Caltrops {"damage" 2}]}
        actions (-> (ActionFactoryBuilder)
                    (.with-trapping-factory 
                     (-> (TrappingFactoryBuilder)
                         (.with-trap-creator (get-trap-creator trap-config))
                         (.build)))
                    (.build))
        character (-> (CharacterBuilder)
                      (.build))
        level (-> (LevelBuilder)
                  (.with-character character #t(5 5))
                  (.build))               
        trap-bag (-> (ItemBuilder)
                     (.with-trap :name "caltrops"
                                 :count 1)
                     (.build))
        large-trap-bag (-> (ItemBuilder)
                           (.with-trap :name "caltrops"
                                       :count 2)
                           (.build))]
    (.append character.inventory trap-bag)
    (.append character.inventory large-trap-bag)
    (set-action-factory actions)
    {:character character
     :level level
     :trap-bag trap-bag
     :large-trap-bag large-trap-bag}))

(defn test-placing-trap-item []
  "placing a trap item is possible"
  (let [context (setup)
        level (:level context)
        character (:character context)
        trap-bag (:trap-bag context)]
    (place-trap character trap-bag)
    (assert-that (get-traps level character.location)
                 (has-length 1))))

(defn test-placing-natural-trap []
  "some creatures are able to create natural traps"
  (let [context (setup)
        level (:level context)
        character (:character context)]
    (place-natural-trap character "caltrops")
    (assert-that (get-traps level character.location)
                 (has-length 1))))

(defn test-placing-nonexistent-bag []
  "placing trap that character doesn't have is not possible"
  (let [context (setup)
        level (:level context)
        character (:character context)        
        trap-bag (-> (ItemBuilder)
                     (.with-trap :name "caltrops"
                                 :count 1)
                     (.build))]
    (assert-that (trapping-legal? character trap-bag)
                 (is- (equal-to False)))))

(defn test-using-simple-item-as-trap []
  "only trap items can be used in trapping"
  (let [context (setup)
        level (:level context)
        character (:character context)
        trap-bag (-> (ItemBuilder)                      
                     (.build))]
    (.append character.inventory trap-bag)
    (assert-that (trapping-legal? character trap-bag)
                 (is- (equal-to False)))))

(defn test-placing-trap-advances-time []
  "placing trap advances time"
  (let [context (setup)
        level (:level context)
        character (:character context)
        trap-bag (:trap-bag context)
        old-tick character.tick]
    (place-trap character trap-bag)
    (assert-that character.tick (is- (greater-than old-tick)))))

(defn test-using-trap-bag-decreses-count []
  "using trap bag decreses amount of traps in it"
  (let [context (setup)
        level (:level context)
        character (:character context)
        trap-bag (:large-trap-bag context)
        old-count trap-bag.trap-data.count]    
    (place-trap character trap-bag)
    (assert-that trap-bag.trap-data.count (is- (less-than old-count)))))

(defn test-empty-trap-bag-is-removed []
  "trap bag is discarded after it's empty"
  (let [context (setup)
        level (:level context)
        character (:character context)
        trap-bag (:trap-bag context)]    
    (place-trap character trap-bag)
    (assert-that character.inventory (is-not- (has-item trap-bag)))))
