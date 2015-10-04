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

(require pyherc.data.effects.macros)

(import [pyherc.data.damage [new-damage]]
        [pyherc.events [new-damage-added-event new-damage-ended-event
                        new-damage-triggered-event]])

(effect-dsl)

(effect DamageEffect "damage"
        [damage damage-type target]
        :trigger (let [[dmg (new-damage [#t(damage damage-type)])]
                       [damage-caused (dmg target)]]
                   (.raise-event target
                                 (new-damage-triggered-event :target target
                                                             :damage damage-caused
                                                             :damage-type damage-type))
                   (.check-dying dying-rules target))
        :add-event (new-damage-added-event :target target
                                           :effect self)
        :remove-event (new-damage-ended-event :target target
                                              :effect self))
