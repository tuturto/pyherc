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

(import [pyherc.generators.level [ItemAdder]])

;; item_adders = [ItemAdder(item_generator, item_adder_config, rng)]
;; item_adders = item_lists(item_generator, [item_by_type(0, 1, "tome"), item_by_type(0, 2, "weapon"), item_by_type(2, 4, "food")], [item_by_type(0, 3, "weapon"), item_by_type(0, 3, "armour")], rng)

(defn item-lists [item-generator rng &rest items]
  (ap-map (ItemAdder item-generator it rng) items))


