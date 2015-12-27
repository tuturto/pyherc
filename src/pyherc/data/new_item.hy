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


(defn weapon? [item]
  "check if this is a weapon"
  (in "weapon" item.tags))

(defn armour? [item]
  "check if this is an armour"
  (in "armour" item.tags))

(defn potion? [item]
  "check if this is a potion"
  (in "potion" item.tags))

(defn ammunition? [item]
  "check if this is ammunition"
  (in "ammunition" item.tags))

(defn food? [item]
  "check if this is food"
  (in "food" item.tags))

(defn trap-bag? [item]
  "check if this is trap bag"
  (in "trap bag" item.tags))

(defn boots? [item]
  "check if these are boots"
  (in "boots" item.tags))

(defn armour-speed-modifier [character]
  "how much armour worn by character affect their speed"
  (if character.inventory.armour
    character.inventory.armour.armour-data.speed-modifier
    1))

(defn boots-speed-modifier [character]
  "how much boots worn by character affect their speed"
  (if character.inventory.boots
    character.inventory.boots.boots-data.speed-modifier
    1))

(defn current-weapon [character]
  "get currently used weapon"
  character.inventory.weapon)

(defn current-ammunition [character]
  "get currently used ammunition"
  (if character.inventory.projectiles
    character.inventory.projectiles
    nil))
