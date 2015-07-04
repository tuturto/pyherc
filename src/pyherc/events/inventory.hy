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

(defn new-pick-up-event [character item]
  "create event to signify picking up an item"
  {:event-type "pick up"
   :level character.level
   :location character.location
   :character character
   :item item})

(defn new-drop-event [character item]
  "create event to signify dropping an item"
  {:event-type "drop"
   :level character.level
   :location character.location
   :character character
   :item item})

(defn new-equip-event [character item]
  "create event to signify equipping an item"
  {:event-type "equip"
   :level character.level
   :location character.location
   :character character
   :item item})

(defn new-unequip-event [character item]
  "create event to signify unequipping an item"
  {:event-type "unequip"
   :level character.level
   :location character.location
   :character character
   :item item})
