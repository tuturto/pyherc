;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2014 Tuukka Turto
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

(require hy.contrib.anaphoric)
(require pyherc.aspects)
(require pyherc.macros)
(import [pyherc.aspects [log-debug]]
        [pyherc.data.features [clear-grave]])

(defclass ExhumeAction []
  [[--init-- #d(fn [self character grave]
                 "default constructor"
                 (-> (super) (.--init--))
                 (setv self.character character)
                 (setv self.grave grave)
                 nil)]
   [legal? #d(fn [self]
               "check if action is possible to perform"
               (using-spade? self.character))]
   [execute #d(fn [self]
                "execute the action"
                (when (.legal? self)
                  (clear-grave self.grave)
                  ))]])

(defn using-spade? [character]
  "check if this character is currently using a spade"
  (let [[weapon character.inventory.weapon]]
    (if (= weapon nil) false
        (when (in :spade weapon.tags) true))))
