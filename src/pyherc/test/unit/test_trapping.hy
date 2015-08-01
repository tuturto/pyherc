;; -*- coding: utf-8 -*-

;;   Copyright 2010-2015 Tuukka Turto
;;
;;   This file is part of pyherc.
;;
;;   pyherc is free software: you can redistribute it and/or modify
;;   it under the terms of the GNU General Public License as published by
;;   the Free Software Foundation, either version 3 of the License, or
;;   (at your option) any later version.
;;
;;   pyherc is distributed in the hope that it will be useful,
;;   but WITHOUT ANY WARRANTY; without even the implied warranty of
;;   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;   GNU General Public License for more details.
;;
;;   You should have received a copy of the GNU General Public License
;;   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

(require pyherc.macros)

(import [pyherc.data [get-traps]]
        [pyherc.data.traps [Caltrops]]
        [pyherc.generators [get-trap-creator]]
        [pyherc.rules [place-trap place-natural-trap can-place-trap]]
        [pyherc.test.builders [ActionFactoryBuilder CharacterBuilder LevelBuilder
                               ItemBuilder TrappingFactoryBuilder]]
        [hamcrest [assert-that has-length is- equal-to greater-than less-than has-item]]
        [hamcrest [is-not :as is-not-]])

(defn setup []
  "setup test case"
  (let [[trap-config {"caltrops" [Caltrops {"damage" 2}]}]
        [actions (-> (ActionFactoryBuilder)
                     (.with-trapping-factory 
                      (-> (TrappingFactoryBuilder)
                          (.with-trap-creator (get-trap-creator trap-config))
                          (.build)))
                     (.build))]
        [character (-> (CharacterBuilder)
                       (.build))]
        [level (-> (LevelBuilder)
                   (.with-character character #t(5 5))
                   (.build))]               
        [trap-bag (-> (ItemBuilder)
                      (.with-trap :name "caltrops"
                                  :count 1)
                      (.build))]
        [large-trap-bag (-> (ItemBuilder)
                            (.with-trap :name "caltrops"
                                        :count 2)
                            (.build))]]
    (.append character.inventory trap-bag)
    (.append character.inventory large-trap-bag)
    {:actions actions
     :character character
     :level level
     :trap-bag trap-bag
     :large-trap-bag large-trap-bag}))

(defn test-placing-trap-item []
  "placing a trap item is possible"
  (let [[context (setup)]
        [level (:level context)]
        [character (:character context)]
        [trap-bag (:trap-bag context)]
        [actions (:actions context)]]
    (place-trap character trap-bag actions)
    (assert-that (get-traps level character.location)
                 (has-length 1))))

(defn test-placing-natural-trap []
  "some creatures are able to create natural traps"
  (let [[context (setup)]
        [level (:level context)]
        [character (:character context)]
        [actions (:actions context)]]
    (place-natural-trap character "caltrops" actions)
    (assert-that (get-traps level character.location)
                 (has-length 1))))

(defn test-placing-nonexistent-bag []
  "placing trap that character doesn't have is not possible"
  (let [[context (setup)]
        [level (:level context)]
        [character (:character context)]
        [actions (:actions context)]
        [trap-bag (-> (ItemBuilder)
                      (.with-trap :name "caltrops"
                                  :count 1)
                      (.build))]]
    (assert-that (can-place-trap character trap-bag actions)
                 (is- (equal-to false)))))

(defn test-using-simple-item-as-trap []
  "only trap items can be used in trapping"
  (let [[context (setup)]
        [level (:level context)]
        [character (:character context)]
        [actions (:actions context)]
        [trap-bag (-> (ItemBuilder)                      
                      (.build))]]
    (.append character.inventory trap-bag)
    (assert-that (can-place-trap character trap-bag actions)
                 (is- (equal-to false)))))

(defn test-placing-trap-advances-time []
  "placing trap advances time"
  (let [[context (setup)]
        [level (:level context)]
        [character (:character context)]
        [actions (:actions context)]
        [trap-bag (:trap-bag context)]
        [old-tick character.tick]]
    (place-trap character trap-bag actions)
    (assert-that character.tick (is- (greater-than old-tick)))))

(defn test-using-trap-bag-decreses-count []
  "using trap bag decreses amount of traps in it"
  (let [[context (setup)]
        [level (:level context)]
        [character (:character context)]
        [actions (:actions context)]
        [trap-bag (:large-trap-bag context)]
        [old-count trap-bag.trap-data.count]]    
    (place-trap character trap-bag actions)
    (assert-that trap-bag.trap-data.count (is- (less-than old-count)))))

(defn test-empty-trap-bag-is-removed []
  "trap bag is discarded after it's empty"
  (let [[context (setup)]
        [level (:level context)]
        [character (:character context)]
        [actions (:actions context)]
        [trap-bag (:trap-bag context)]]    
    (place-trap character trap-bag actions)
    (assert-that character.inventory (is-not- (has-item trap-bag)))))
