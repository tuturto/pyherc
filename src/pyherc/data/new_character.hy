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

(defn skill-ready? [character skill]
  "check if the cooldown of a skill has passed"
  (<= (cooldown character skill) 0))

(defn cooldown [character skill &optional limit]
  "cooldown of a specific skill for a character"
  (when limit
    (assoc character.cooldowns skill limit))
  (when (not (in skill character.cooldowns))
    (assoc character.cooldowns skill 0))
  (get character.cooldowns skill))

(defn visited-levels↜ [character]
  "get generator for visited levels of this character"
  (genexpr x [x character.visited-levels]))

(defn visited-levels [character]
  "get list of visited levels for this character"
  character.visited-levels)

(defn add-visited-level [character level]
  "add level to visited levels list"
  (when (not (in level character.visited-levels))
    (.append character.visited-levels level)))

(defn speed-modifier [character]
  "get total speed modifier for this character"
  (let [[speed-mod 1.0]]
    (when character.inventory.armour
      (setv speed-mod (* speed-mod character.inventory.armour.armour-data.speed-modifier)))
    (when character.inventory.boots
      (setv speed-mod (* speed-mod character.inventory.boots.boots-data.speed-modifier)))
    speed-mod))

(defn movement-mode [character]
  "get effective movement mode, taking special items into account"
  (let [[modes (set (list-comp x.mode [x (.get-effects character)]
                               (= x.effect-name "movement mode modifier")))]]
    (if modes
      (if (in "fly" modes)
        "fly"
        "walk")
      "walk")))
