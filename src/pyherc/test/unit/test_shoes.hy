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

(import [pyherc.data [boots?]]
        [pyherc.ports [equip set-action-factory]]
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
    (set-action-factory actions)
    {:character character
     :boots boots}))

(defn test-wearing-boots []
  "boots can be worn"
  (let [[context (setup)]
        [character (:character context)]
        [boots (:boots context)]]
    (equip character boots)
    (assert-that character.inventory.boots (is- (equal-to boots)))))

(defn test-item-main-type-for-boots []
  "boots should have item main type set correctly"
  (let [[context (setup)]
        [boots (:boots context)]]
    (assert-that (boots? boots) (is- (equal-to true)))))
