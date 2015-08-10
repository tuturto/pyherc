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

(require pyherc.macros)

(import [pyherc.data.effects.effect [Effect]])

(defclass MovementModeModifier [Effect]
  "effect to modify movement mode"
  [[--init-- (fn [self mode duration frequency tick icon title description]
               "default initializer"
               (super-init :duration duration
                           :frequency frequency
                           :tick tick
                           :icon icon
                           :title title
                           :description description)
               (setv self.mode mode)
               (setv self.multiple-allowed true)
               nil)]
   [get-add-event (fn [self]
                    "get event describing adding of this effect")]
   [get-removal-event (fn [self]
                        "get event describing removal of this effect")]])
