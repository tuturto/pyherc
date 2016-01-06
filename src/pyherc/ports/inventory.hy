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

(import [pyherc.rules.public [ActionParameters]]
        [pyherc.ports [interface]])

(defn pick-up [character item]
  "pick up item"
  (let [[action (.get-action interface.*factory*
                             (InventoryParameters character item "pick up"))]]
    (when (.legal? action)
      (.execute action))))

(defn picking-up-legal? [character item]
  true) ;; TODO: implement

(defn drop-item [character item]
  "drop item from inventory"
  (let [[action (.get-action interface.*factory*
                             (InventoryParameters character item "drop"))]]
    (when (.legal? action)
      (.execute action))))

(defn dropping-item-legal? [character item]
  true) ;; TODO: implement

(defn equip [character item]
  "wear item from inventory"
  (let [[action (.get-action interface.*factory*
                             (InventoryParameters character item "equip"))]]
    (when (.legal? action)
      (.execute action))))

(defn equipping-legal? [character item]
  true) ;; TODO: implement

(defn unequip [character item]
  "unequip item"
  (let [[action (.get-action interface.*factory*
                             (InventoryParameters character item "unequip"))]]
    (when (.legal? action)
      (.execute action))))

(defn unequipping-legal? [character item]
  true) ;; TODO: implement

(defclass InventoryParameters [ActionParameters]
  [[--init-- (fn [self character item sub-action]
               (super-init)
               (set-attributes character item sub-action)
               (setv self.action-type "inventory")
               nil)]])
