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

(defmacro item [name description cost weight icons types rarity]  
  `(ItemConfiguration ~name ~cost ~weight ~icons ~types
                      ~rarity nil nil nil nil ~description))

(defmacro tome [name &rest content]
  `(ItemConfiguration ~name 
                      100 1 ["tied-scroll"]
                      ["tome"] "rare" nil nil nil nil
                      (.join " " [~@content])))

(defmacro scroll [name &rest content]
  `(ItemConfiguration ~name 
                      50 1 ["tied-scroll"]
                      ["scroll"] "rare" nil nil nil nil
                      (.join " " [~@content])))

(defmacro items-list [&rest items]
  `(defn init-items [context]
     [~@items]))
