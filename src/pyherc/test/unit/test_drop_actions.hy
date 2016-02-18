;; -*- coding: utf-8 -*-
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

(require archimedes)
(require pyherc.macros)

(import [pyherc.ports [set-action-factory drop-item]]
        [pyherc.test.builders [LevelBuilder CharacterBuilder ItemBuilder
                               ActionFactoryBuilder]]
        [hamcrest [assert-that is- equal-to is-not :as is-not- is-in
                   greater-than]]
        [hypothesis.strategies [integers tuples]])

(background default
            [level (-> (LevelBuilder)
                       (.with-size #t(20 20))
                       (.build))]
            [item (-> (ItemBuilder)
                      (.build))]
            [character (-> (CharacterBuilder)
                           (.with-item item)
                           (.with-level level)
                           (.with-location #t(5 5))
                           (.build))]
            [_ (set-action-factory (-> (ActionFactoryBuilder)
                                       (.with-inventory-factory)
                                       (.build)))])

(fact "dropped item is removed from inventory"
      (with-background default [character item]
        (drop-item character item)
        (assert-that item (is-not- (is-in (. character inventory))))))

(fact "dropped item is added on level"
      (with-background default [character item level]
        (drop-item character item)
        (assert-that (. item level) (is- (equal-to level)))))

(fact "dropped item is in same location as character dropping it"
      (variants :coordinates (tuples (integers :min-value 0 :max-value 19)
                                     (integers :min-value 0 :max-value 19)))
      (with-background default [character item level]
        (setv (. character location) coordinates)
        (drop-item character item)
        (assert-that (. item location) (is- (equal-to (. character location))))))

(fact "dropping an item takes time"
      (with-background default [character item]
        (let [[old-time (. character tick)]]
          (drop-item character item)
          (assert-that (. character tick)
                       (is- (greater-than old-time))))))
