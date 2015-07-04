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

(defn new-attack-hit-event [type attacker target damage]
  "create new event to signify landing an attack"
  {:event-type "attack hit"
   :level attacker.level
   :location attacker.location
   :type type
   :attacker attacker
   :target target
   :damage damage})

(defn new-attack-miss-event [type attacker target]
  "create new event to signify missing an attack"
  {:event-type "attack miss"
   :level attacker.level
   :location attacker.location
   :type type
   :attacker attacker
   :target target})

(defn new-attack-nothing-event [attacker]
  "create new event to signify attacking nothing"
  {:event-type "attack nothing"
   :level attacker.level
   :location attacker.location
   :attacker attacker})

