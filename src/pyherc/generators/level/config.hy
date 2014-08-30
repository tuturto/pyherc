;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2014 Tuukka Turto
;;
;;  This file is part of pyherc.
;;
;;  pyherc is free software: you can redistribute it and/or modify
;;  it under the terms of the GNU General Public License as published by
;;  the Free Software Foundation, either version 3 of the License, or
;;  (at your option) any later version.
;;
;;  pyherc is distributed in the hope that it will be useful,
;;  but WITHOUT ANY WARRANTY; without even the implied warranty of
;;  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;  GNU General Public License for more details.
;;
;;  You should have received a copy of the GNU General Public License
;;  along with pyherc.  If not, see <http://www.gnu.org/licenses/>.


(defn new-dungeon []
  "create new instance of dungeon config"
  {})

(defn add-level [dungeon level]
  "add new level config into dungeon config"
  (assoc dungeon-config (:level-name level-config) level-config))

(defn new-level [level-name room-generators partitioners decorators
                 item-adders portal-config context model]
  "create new instance of level config"
  {:level-name level-name
   :room-generators room-generators
   :partitioners partitioners
   :decorators decorators
   :item-adders item-adders
   :portal-config portal-config
   :context context
   :model model})
