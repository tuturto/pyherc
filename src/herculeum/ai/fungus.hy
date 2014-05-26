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
(require hy.contrib.anaphoric)
(import [pyherc.aspects [log-debug]]
	[herculeum.ai.basic [attack-enemy wait]]
        [pyherc.data [get-character]]
        [pyherc.data.geometry [area-around]]
        [pyherc.rules.mitosis.interface [perform-mitosis mitosis-legal?]]
        [pyherc.rules.metamorphosis.interface [morph morph-legal?]]
	[random [choice]])

(setv __doc__ "module for AI routines for fungus")

(defclass FungusAI []
  [[__doc__ "AI routine for fungus"]
   [character None]
   [--init-- (fn [self character]
           "default constructor"
           (.--init-- (super FungusAI self))
           (setv self.character character)
	   None)]
   [act (fn [self model action-factory rng]
      "check the situation and act accordingly"
      (fungus-act self model action-factory rng))]])

(defclass GreatFungusAI []
  [[__doc__ "AI routine for great fungus"]
   [character None]
   [--init-- (fn [self character]
           "default constructor"
           (.--init-- (super GreatFungusAI self))
           (setv self.character character)
	   None)]
   [act (fn [self model action-factory rng]
      "check the situation and act accordingly"
      (great-fungus-act self model action-factory rng))]])


#d(defn fungus-act [ai model action-factory rng]
    (let [[enemies (adjacent-enemies ai)]]
      (if enemies
	(attack-enemy ai (choice enemies) action-factory rng)
        (rarely
         (cond [(mitosis-legal? ai.character action-factory)
                (perform-mitosis ai.character action-factory)]
               [(and (morph-legal? ai.character "great fungus" action-factory)
                     (>= (count (adjacent-friends ai)) 6))
                (morph-great-fungi ai action-factory)]
               [true (wait ai)])
         (wait ai)))))

#d(defn great-fungus-act [ai model action-factory rng]
    (let [[enemies (adjacent-enemies ai)]]
      (if enemies
	(attack-enemy ai (choice enemies) action-factory rng)
        (wait ai))))

#d(defn morph-great-fungi [ai action-factory]
    "morph character into a great fungi"
    (morph ai.character "great fungus" action-factory 
           (adjacent-friends ai)))

#d(defn adjacent-friends [ai]
    "get list of friends adjacent to given ai"
    (let [[character ai.character]
          [level character.level]
          [location character.location]
          [characters (ap-map (get-character level it) (area-around location))]]
      (ap-filter (friend? character it) characters)))

#d(defn characters-around [level location]
    "get characters around given location"
    (ap-filter it
               (ap-map (get-character level it)
                       (area-around location))))

#d(defn friend? [character-0 character-1]
    "are two characters friends"
    (and character-0 character-1
         (= character-0.name character-1.name)))

#d(defn adjacent-enemies [ai]
    "get list of enemies adjacent to given ai"
    (let [[loc ai.character.location]
	  [level ai.character.level]
	  [monsters []]]
      (for [x (range (- (x-coordinate loc) 1) (+ (x-coordinate loc) 2))]
	(for [y (range (- (y-coordinate loc) 1) (+ (y-coordinate loc) 2))]
	  (let [[creature (get-character level #t(x y))]]
	    (when (and creature
		       (!= creature ai.character)
		       (!= creature.name ai.character.name))
	      (.append monsters creature)))))
      monsters))
