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

(require pyherc.aspects)
(require pyherc.macros) ;; TODO: remove this if xor ever lands Hy

(import [pyherc.aspects [log-debug]]
        [pyherc.data [add-trap trap-bag?]]
        [pyherc.data.constants [Duration]])

(defclass TrappingAction []
  "Action of placing a trap"
  [[--init-- #d(fn [self character trap-bag trap-name trap-creator]
                 "default constructor"
                 (-> (super) (.--init--))
                 (assert character)
                 (assert (xor trap-bag trap-name))
                 (assert trap-creator)
                 (setv self.character character)
                 (setv self.trap-bag trap-bag)
                 (setv self.trap-name trap-name)
                 (setv self.trap-creator trap-creator)
                 nil)]
   [legal? #d(fn [self]
               "check if action is possible to perform"
               (if self.trap-bag
                 (and (in self.trap-bag self.character.inventory)
                      (trap-bag? self.trap-bag))
                 true))]
   [execute #d(fn [self]
                "execute the action"
                (when (.legal? self)
                  (let [[character self.character]
                        [level character.level]
                        [location character.location]
                        [trap (get-trap self.trap-creator
                                        self.trap-bag
                                        self.trap-name)]]
                    (add-trap level location trap)
                    (when self.trap-bag
                      (setv self.trap-bag.trap-data.count 
                            (dec self.trap-bag.trap-data.count))
                      (when (< self.trap-bag.trap-data.count 1)
                        (character.inventory.remove self.trap-bag)))
                    (.add-to-tick character Duration.normal))))]])

(defn get-trap [trap-creator trap-bag trap-name]
  "get trap instance"
  (if trap-bag
    (trap-creator trap-bag.trap-data.trap-name)
    (trap-creator trap-name)))
