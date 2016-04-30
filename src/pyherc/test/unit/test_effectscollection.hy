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
(require archimedes)

(import [hamcrest [assert-that equal-to is- is-in is-not :as is-not!]]
        [pyherc.test.matchers [has-effect has-effect-handle
                               has-effect-handles]])

(import [pyherc.data.effects [EffectsCollection]]
        [pyherc.test.builders [EffectBuilder EffectHandleBuilder]])

(defn test-adding-effect-handle []
  "Effect handle can be added and retrieved from collection"
  (let [[handle (-> (EffectHandleBuilder)
                    (.build))]
        [collection (EffectsCollection)]]
    (.add-effect-handle collection handle)
    (assert-that collection (has-effect-handle handle))))

(defn test-adding-multiple-handles []
  "Multiple handles can be added without key collisions"
  (let [[handle₁ (-> (EffectHandleBuilder)
                     (.with-effect "heal")
                     (.build))]
        [handle₂ (-> (EffectHandleBuilder)
                     (.with-effect "bless")
                     (.build))]
        [collection (EffectsCollection)]]
    (.add-effect-handle collection handle₁)
    (.add-effect-handle collection handle₂)
    (assert-that collection (has-effect-handles [handle₁ handle₂]))))

(defn test-returning-only-specific-handles []
  "Effect handles can be retrieved by their trigger"
  (let [[handle₁ (-> (EffectHandleBuilder)
                     (.with-trigger "on drink")
                     (.build))]
        [handle₂ (-> (EffectHandleBuilder)
                     (.with-trigger "on bash")
                     (.build))]
        [collection (EffectsCollection)]]
    (.add-effect-handle collection handle₁)
    (.add-effect-handle collection handle₂)
    (assert-that handle₂ (is-in (.get-effect-handles collection "on bash")))))

(defn test-no-matching-trigger-for-handle []
  "Effects collection returns an empty list when trigger does not match"
  (let [[handle (-> (EffectHandleBuilder)
                    (.with-trigger "on sleep")
                    (.build))]
        [collection (EffectsCollection)]]
    (.add-effect-handle collection handle)
    (assert-that (.get-effect-handles collection "on kick")
                 (is- (equal-to [])))))

(defn test-removing-effect-handle []
  "Effect handle can be removed from collection"
  (let [[handle (-> (EffectHandleBuilder)
                    (.build))]
        [collection (EffectsCollection)]]
    (.add-effect-handle collection handle)
    (.remove-effect-handle collection handle)
    (assert-that collection (is-not! (has-effect-handle handle)))))

(defn test-adding-effects []
  "Effect can be added into collection"
  (let [[effect (-> (EffectBuilder)
                    (.build))]
        [collection (EffectsCollection)]]
    (.add-effect collection effect)
    (assert-that collection (has-effect effect))))

(defn test-removing-expired-effects []
  "Expired effects can be removed automatically"
  (let [[effect (-> (EffectBuilder)
                    (.with-duration 0)
                    (.build))]
        [collection (EffectsCollection)]]
    (.add-effect collection effect)
    (.remove-expired-effects collection)
    (assert-that collection (is-not! (has-effect effect)))))
