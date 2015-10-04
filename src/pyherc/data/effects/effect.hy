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

(import [pyherc.events [new-effect-added-event new-effect-removed-event]])

(require pyherc.macros)

(defclass Effect []
  "class representing effects"
  [[--init-- (fn [self duration frequency tick icon title description]
               "default initializer"
               (super-init)
               (set-attributes duration frequency tick icon title description)
               (setv self.effect-name "effect")
               (setv self.multiple-allowed false)
               nil)]
   [trigger (fn [self dying-rules]
              "trigger the effect"
              (.do-trigger self dying-rules)
              (.post-trigger self))]
   [do-trigger (fn [self dying-rules]
                 "override this method to contain logic of the effect"
                 nil)]
   [post-trigger (fn [self]
                   "do house keeping after effect has been triggered"
                   (when (is-not self.duration nil)
                     (setv self.tick self.frequency)
                     (setv self.duration (- self.duration self.frequency))))]
   [get-add-event (fn [self]
                    "get event describing adding this effect"
                    (new-effect-added-event self))]
   [get-removal-event (fn [self]
                        "get event describing removing this effect"
                        (new-effect-removed-event self))]])

(defclass EffectHandle []
  "handle that can be used to construct effects"
  [[--init-- (fn [self trigger effect parameters charges]
               "default initializer"
               (super-init)
               (set-attributes trigger effect parameters charges)
               nil)]
   [--str-- (fn [self]
              "string representation of this object"
              (.format "trigger: {0}, effect: {1}, parameters: {2}, charges: {3}"
                       self.trigger self.effect self.parameters self.charges))]])
