;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2015 Tuukka Turto
;;
;;  This file is part of pyherc.
;;
;;  pyherc is free software: you can redistribute it and/or modify
;;  it under the terms of the GNU General Public License as published by
;;  the Free Software Foundation either version 3 of the License or
;;  (at your option) any later version.
;;
;;  pyherc is distributed in the hope that it will be useful
;;  but WITHOUT ANY WARRANTY; without even the implied warranty of
;;  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;  GNU General Public License for more details.
;;
;;  You should have received a copy of the GNU General Public License
;;  along with pyherc.  If not see <http://www.gnu.org/licenses/>.

(require pyherc.macros)

(import [pyherc.generators.level [new-level]]
        [pyherc.generators.level.partitioners [binary-space-partitioning]])
(import [herculeum.config.floor_builders [floor-builder wall-builder
                                          floor-swapper]]
        [herculeum.config.room_generators [square-room]])

(defn init-level [rng item-generator creature-generator level-size context]
  [(new-level "upper mines" (rooms rng) (partitioners rng) (decorators rng)
              (item-adders rng) (creature-adders rng) (portal-configurations))])

(defn rooms [rng]
  [(square-room "ground_soil3" "ground_soil3" rng)])

(defn partitioners [rng]
  [(binary-space-partitioning #t(80 40) #t(11 11) rng)])

(defn decorators [rng]
  [(wall-builder "wall_rubble2")
   (floor-builder "ground_soil3")
   (floor-swapper "ground_soil3" "ground_rock3" 25 rng)])

(defn item-adders [rng]
  [])

(defn creature-adders [rng]
  [])

(defn portal-configurations []
  [])
