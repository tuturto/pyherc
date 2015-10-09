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

(defn damage-triggered [target damage damage-type]
  "create new event to signify damage was dealt"
  {:event-type "damage triggered"
   :level target.level
   :location target.location
   :target target
   :damage damage
   :damage-type damage-type})

(defn damage-added [target effect]
  "create event to signify damage effect was added"
  {:event-type "damage started"
   :level target.level
   :location target.location
   :target target
   :effect effect})

(defn damage-ended [target effect]
  "create event to signify damage effect is over"
  {:event-type "damage ended"
   :level target.level
   :location target.location
   :target target
   :effect effect})

