;; -*- coding: utf-8 -*-

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

(require pyherc.aspects)
(import [pyherc.rules.public [ActionParameters]]
        [pyherc.aspects [log-debug log-info]])

(defn place-trap [character trap-bag action-factory]
  "place trap"
  (let [[action (.get-action action-factory
                             (TrappingParameters character :trap-bag trap-bag))]]
    (when (.legal? action)
      (.execute action))))

(defn place-natural-trap [character trap-name action-factory]
  "place trap without using any items"
  (let [[action (.get-action action-factory
                             (TrappingParameters character :trap-name trap-name))]]
    (when (.legal? action)
      (.execute action))))

(defn can-place-trap [character trap-bag action-factory]
  "check if character can place a trap"
  (let [[action (.get-action action-factory
                             (TrappingParameters character :trap-bag trap-bag))]]
    (.legal? action)))

(defn can-place-natural-trap [character trap-name action-factory]
  "check if character can place a natural trap"
  (let [[action (.get-action action-factory
                             (TrappingParameters character :trap-name trap-name))]]
    (.legal? action)))

(defclass TrappingParameters [ActionParameters]
  "class controlling creation of TrappingAction"
  [[--init-- #d(fn [self character &optional [trap-bag nil] [trap-name nil]]
                 (-> (super) (.--init--))
                 (setv self.character character)
                 (setv self.action-type "trapping")
                 (setv self.trap-bag trap-bag)
                 (setv self.trap-name trap-name)
                 nil)]])
