;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2015 Tuukka Turto
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

(import [pyherc.generators [ItemConfiguration TrapConfiguration]])

(defmacro items-dsl []
  `(import [herculeum.config.levels.macros [item tome scroll trap-bag]]))

(defn item [name description cost weight icons types rarity]  
  (ItemConfiguration :name name
                     :cost cost
                     :weight weight
                     :icons icons
                     :types types
                     :rarity rarity
                     :description description))

(defn tome [name &rest content]
  (ItemConfiguration :name name 
                     :cost 100
                     :weight 1
                     :icons ["tied-scroll"]
                     :types ["tome" "hint"]
                     :rarity "rare"
                     :description (.join " " content)))

(defn scroll [name &rest content]
  (ItemConfiguration :name name 
                     :cost 50
                     :weight 1
                     :icons ["tied-scroll"]
                     :types ["scroll" "hint"]
                     :rarity "uncommon"
                     :description (.join " " content)))

(defn trap-bag [name description trap-name count cost weight icons types rarity]
  (ItemConfiguration :name name
                     :cost cost
                     :weight weight
                     :icons icons
                     :types types
                     :rarity rarity
                     :trap-configuration (TrapConfiguration trap-name count)
                     :description description))

(defmacro items-list [&rest items]
  `(defn init-items [context]
     [~@items]))

