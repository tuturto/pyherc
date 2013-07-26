;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2013 Tuukka Turto
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

(setv __doc__ "module for common AI routines")

(import [pyherc.aspects [logged]]
	[random]
	[math [sqrt]])

(require pyherc.ai.macros)

(with-decorator logged
  (defn fight-in-melee [attack-routine close-in-routine ai action-factory]
    "routine to make character to fight"
    (let [[own-location ai.character.location]
	  [enemy (second ai.mode)]
	  [enemy-location enemy.location]
	  [distance (distance-between own-location enemy-location)]]
      (if (< distance 2)
	(attack-routine ai enemy action-factory (.Random random))
	(close-in-routine ai enemy action-factory)))))

(defn distance-between [start end]
  "calculate distance between two locations"
  (let [[dist-x (- (first start) (first end))]
	[dist-y (- (second start) (second end))]]
    (sqrt (+ (pow dist-x 2)
          (pow dist-y 2)))))
