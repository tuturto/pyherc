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

(defn poison-triggered [target damage]
  "create event to signify poison was triggered"
  {:event-type "poison triggered"
   :level target.level
   :location target.location
   :target target
   :damage damage})

(defn poison-added [target effect]
  "create event to signify a character was poisoned"
  {:event-type "poisoned"
   :level target.level
   :location target.location
   :target target
   :effect effect})

(defn poison-ended [target effect]
  "create event to signify poisoning has ended"
  {:event-type "poison ended"
   :level target.level
   :location target.location
   :target target
   :effect effect})
