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

(import [hamcrest [assert-that contains-inanyorder]]
        [pyherc.generators.level [new-dungeon new-level add-level
                                  room-generators]])

(defn setup-context []
  "setup test dungeon configuration"
  (let [[dungeon (new-dungeon)]
        [level₀ (new-level "level₀"
                           [:room₀ :room₁]
                           [:partitioner₀]
                           [:decorator₀ :decorator₁]
                           [:items₀]
                           :portal-config₀)]
        [level₁ (new-level "level₁"
                           [:room₁ :room₂]
                           [:partitioner₁]
                           [:decorator₂ :decorator₃]
                           [:items₁]
                           :portal-config₁)]]
    (add-level dungeon level₀)
    (add-level dungeon level₁)
    {:dungeon dungeon
     :level₀ level₀
     :level₁ level₁}))

(defn test-room-config []
  "test that room configuration can be retrieved"
  (let [[context (setup-context)]
        [dungeon (:dungeon context)]]
    (assert-that (room-generators dungeon "level₀")
                 (contains-inanyorder :room₀ :room₁))
    (assert-that (room-generators dungeon "level₁")
                 (contains-inanyorder :room₁ :room₂))))
