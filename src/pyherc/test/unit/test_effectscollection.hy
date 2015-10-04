;; -*- coding: utf-8 -*-
;;
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
