;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2014 Tuukka Turto
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
(require pyherc.macros)
(require herculeum.ai.macros)
(import [pyherc.aspects [log-debug]]
	[herculeum.ai.basic [attack-enemy wait mitosis]]
	[random [choice]])

(setv __doc__ "module for AI routines for fungus")

(defclass FungusAI []
  [[__doc__ "AI routine for fungus"]
   [character None]
   [mode [:transit None]]
   [--init-- (fn [self character]
           "default constructor"
           (.--init-- (super FungusAI self))
           (setv self.character character)
	   None)]
   [act (fn [self model action-factory rng]
      "check the situation and act accordingly"
      (fungus-act self model action-factory rng))]])

#d(defn fungus-act [ai model action-factory rng]
    (let [[enemies (adjacent-enemies ai)]]
      (if enemies
	(attack-enemy ai (choice enemies) action-factory rng)
	(very-rarely (mitosis ai action-factory)
		     (wait ai)))))

#d(defn adjacent-enemies [ai]
    "get list of enemies adjacent to given ai"
    (let [[loc ai.character.location]
	  [level ai.character.level]
	  [monsters []]]
      (for [x (range (- (x-coordinate loc) 1) (+ (x-coordinate loc) 2))]
	(for [y (range (- (y-coordinate loc) 1) (+ (y-coordinate loc) 2))]
	  (let [[creature (.get-creature-at level #t(x y))]]
	    (when (and creature
		       (!= creature ai.character)
		       (!= creature.name ai.character.name))
	      (.append monsters creature)))))
      monsters))
