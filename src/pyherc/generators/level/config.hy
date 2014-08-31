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
  (assoc dungeon (:level-name level) level))

(defn merge-level [dungeon level]
  "merge new level config into existing dungeon data")

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

(defmacro level-config [component-name dungeon level-name]
 `(genexpr x [x (~component-name (get ~dungeon ~level-name))]))

(defn room-generators [dungeon level-name]
  "get room generators for given level"
  (level-config :room-generators dungeon level-name))

(defn partitioners [dungeon level-name]
  "get level partitioners for given level"
  (level-config :partitioners dungeon level-name))

(defn decorators [dungeon level-name]
  "get level decorators for given level"
  (level-config :decorators dungeon level-name))

(defn item-adders [dungeon level-name]
  "get item adders for given level"
  (level-config :item-adders dungeon level-name))

(defn portals [dungeon level-name]
  "get portal configs"
  (level-config :portal-config dungeon level-name))

(defn context [dungeon level-name]
  "get configuration context"
  (:context (get dungeon level-name)))

(defn model [dungeon level-name]
  "get model"
  (:model (get dungeon level-name)))
