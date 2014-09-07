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

(require hy.contrib.anaphoric)

(defn new-dungeon []
  "create new instance of dungeon config"
  {})

(defn add-level [dungeon level]
  "add new level config into dungeon config"
  (assoc dungeon (:level-name level) level))

(defmacro merge-component-list [component-name dungeon level]
  `(.extend (get (get ~dungeon (:level-name level)) ~component-name)
            (~component-name ~level)))

(defmacro level-config [component-name dungeon level-name]
 `(genexpr x [x (~component-name (get ~dungeon ~level-name))]))

(defn merge-level [dungeon level]
  "merge new level config into existing dungeon data"
  (if (in (:level-name level) dungeon)
    (do (merge-component-list :room-generators dungeon level)
        (merge-component-list :partitioners dungeon level)
        (merge-component-list :decorators dungeon level)
        (merge-component-list :items dungeon level)
        (merge-component-list :characters dungeon level)
        (merge-component-list :portal-config dungeon level))
    (assert false)
    ))

(defn new-level [level-name room-generators partitioners decorators
                 items characters portal-config]
  "create new instance of level config"
  {:level-name level-name
   :room-generators room-generators
   :partitioners partitioners
   :decorators decorators
   :items items
   :characters characters
   :portal-config portal-config})

(defn room-generators [dungeon level-name]
  "get room generators for given level"
  (level-config :room-generators dungeon level-name))

(defn level-partitioners [dungeon level-name]
  "get level partitioners for given level"
  (level-config :partitioners dungeon level-name))

(defn decorators [dungeon level-name]
  "get level decorators for given level"
  (level-config :decorators dungeon level-name))

(defn items [dungeon level-name]
  "get items for given level"
  (level-config :items dungeon level-name))

(defn characters [dungeon level-name]
  "get characters for given level"
  (level-config :characters dungeon level-name))

(defn portals [dungeon level-name]
  "get portal configs"
  (level-config :portal-config dungeon level-name))
