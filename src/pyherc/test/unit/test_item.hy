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

(require pyherc.test.macros)

(import [hamcrest [assert-that is- equal-to is-not :as is-not-
                   contains-inanyorder contains empty has-length]]
        [pyherc.data [weapon? food?]]
        [pyherc.test.builders [ItemBuilder CharacterBuilder
                               ActionFactoryBuilder EffectHandleBuilder]]
        [pyherc.ports [equip unequip set-action-factory]])

(background weapons
            [item (-> (ItemBuilder)
                      (.with-damage 2 "piercing")
                      (.with-name "club")
                      (.build))]
            [character (-> (CharacterBuilder)
                           (.build))]
            [_ (set-action-factory (-> (ActionFactoryBuilder)
                                       (.with-inventory-factory)
                                       (.build)))])
(fact "character can wield weapon"
      (with-background weapons [item character]
        (equip character item)
        (assert-that character.inventory.weapon (is- (equal-to item)))))

(fact "character can unwield weapon"
      (with-background weapons [item character]
        (equip character item)
        (unequip character item)
        (assert-that character.inventory.weapon (is-not- (equal-to item)))))

(fact "weapon worn in hand can be reported as such in its name"
      (with-background weapons [item character]
        (equip character item)
        (assert-that (.get-name item character true) (is- (equal-to "club (weapon in hand)")))))

(fact "item main type depends on tags"
      (assert-that (weapon? (-> (ItemBuilder)
                                (.with-tag "weapon")
                                (.build))))
      (assert-that (food? (-> (ItemBuilder)
                              (.with-tag "food")
                              (.build)))))

(background potions
            [potion (-> (ItemBuilder)
                        (.with-name "healing potion")
                        (.with-appearance "blue potion")
                        (.build))]
            [character (-> (CharacterBuilder)
                           (.build))])

(fact "unknown items are named after their appearance"
      (with-background potions [potion character]
        (assert-that (.get-name potion character) (is- (equal-to "blue potion")))))

(fact "items named by character are reported by their given name"
      (with-background potions [potion character]
        (assoc character.item-memory "healing potion" "doozer potion")
        (assert-that (.get-name potion character) (is- (equal-to "doozer potion")))))

(fact "identified items are reported by their real name instead of appearance"
      (with-background potions [potion character]
        (.identify-item character potion)
        (assert-that (.get-name potion character) (is- (equal-to "healing potion")))))

(background effects
            [effect₁ (-> (EffectHandleBuilder)
                         (.with-trigger "on drink")
                         (.build))]
            [effect₂ (-> (EffectHandleBuilder)
                         (.with-trigger "on break")
                         (.build))]
            [item (-> (ItemBuilder)
                      (.with-effect-handle effect₁)
                      (.with-effect-handle effect₂)
                      (.build))])

(fact "all effects of item can be queried as a list"
      (with-background effects [effect₁ effect₂ item]
        (assert-that (.get-effect-handles item)
                     (contains-inanyorder effect₁ effect₂))))

(fact "effects of item with specific trigger can be queried as a list"
      (with-background effects [effect₂ item]
        (assert-that (.get-effect-handles item "on break")
                     (contains effect₂))))

(fact "when item with no effects is queried, an empty list is returned"
      (with-background effects [item]
        (assert-that (.get-effect-handles item "on hit")
                     (is- (empty)))))

(background charges
            [effect₁ (-> (EffectHandleBuilder)
                         (.with-trigger "on drink")
                         (.with-charges 1)
                         (.build))]
            [effect₂ (-> (EffectHandleBuilder)
                         (.with-trigger "on kick")
                         (.with-charges 2)
                         (.build))]
            [item-with-one-charge (-> (ItemBuilder)
                                      (.with-effect-handle effect₁)
                                      (.build))]
            [item-with-two-charges (-> (ItemBuilder)
                                       (.with-effect-handle effect₁)
                                       (.with-effect-handle effect₂)
                                       (.build))])

(fact "item with single effect has equal amount charges left as the effect"
      (with-background charges [item-with-one-charge]
        (assert-that item-with-one-charge.charges-left
                     (contains 1))))

(fact "charges of item with multiple charges can be retrieved"
      (with-background charges [item-with-two-charges]
        (assert-that item-with-two-charges.charges-left
                     (contains-inanyorder 1 2))))

(fact "minimum and maximum charges left of item can be retrieved"
      (with-background charges [item-with-two-charges]
        (assert-that item-with-two-charges.minimum-charges-left
                     (is- (equal-to 1)))
        (assert-that item-with-two-charges.maximum-charges-left
                     (is- (equal-to 2)))))
