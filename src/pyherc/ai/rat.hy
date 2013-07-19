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

"""
Simple AI for flocking creature

Creature will try to find friends, before attacking the player character
"""

(defclass RatAI []
  [[character None]
  [__init__ (fn [self character] (setv self.character character) None)]
  [act (fn [self model action_factory rng] (rat-act self model action_factory rng))]
  ]
)

(defn rat-act [ai model action_factory rng] (setv ai.character.tick 50))
