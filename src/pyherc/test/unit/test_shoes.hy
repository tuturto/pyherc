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

(import [pyherc.data [boots?]]
        [pyherc.rules [equip]]
        [pyherc.test.builders [ActionFactoryBuilder CharacterBuilder
                               ItemBuilder]]
        [hamcrest [assert-that is- equal-to]])

(defn setup []
  "setup test case"
  (let [[character (-> (CharacterBuilder)
                       (.build))]
        [boots (-> (ItemBuilder)
                   (.with-boots-speed-modifier 1)
                   (.with-boots-damage-reduction 0)
                   (.build))]
        [actions (-> (ActionFactoryBuilder)
                     (.with-inventory-factory)
                     (.build))]]
    {:character character
     :boots boots
     :actions actions}))

(defn test-wearing-boots []
  "boots can be worn"
  (let [[context (setup)]
        [character (:character context)]
        [boots (:boots context)]
        [actions (:actions context)]]
    (equip character boots actions)
    (assert-that character.inventory.boots (is- (equal-to boots)))))

(defn test-item-main-type-for-boots []
  "boots should have item main type set correctly"
  (let [[context (setup)]
        [boots (:boots context)]]
    (assert-that (boots? boots) (is- (equal-to true)))))
