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
