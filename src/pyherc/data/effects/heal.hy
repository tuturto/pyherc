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

(import [pyherc.events [new-heal-added-event new-heal-ended-event
                        new-heal-triggered-event]])

(effect-dsl)

(effect Heal "heal"
        [healing target]
        :trigger (do
                  (setv target.hit-points (+ target.hit-points healing))
                  (when (> target.hit-points target.max-hp)
                    (setv target.hit-points target.max-hp))
                  (.raise-event target (new-heal-triggered-event :target target
                                                                 :healing healing)))
        :add-event (new-heal-added-event :target target
                                         :effect self)
        :remove-event (new-heal-ended-event :target target
                                            :effect self))
