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

(import [pyherc.events [new-poison-added-event new-poison-ended-event
                        new-poison-triggered-event]])

(effect-dsl)

(effect Poison "poison"
        [target damage]
        :trigger (do 
                  (setv target.hit-points (- target.hit-points damage))
                  (.raise-event target (new-poison-triggered-event :target target
                                                                   :damage damage))
                  (.check-dying dying-rules target))
        :add-event (new-poison-added-event :target target
                                           :effect self)
        :remove-event (new-poison-ended-event :target target
                                              :effect self))
