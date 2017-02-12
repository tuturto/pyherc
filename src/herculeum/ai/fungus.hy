;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2017 Tuukka Turto
;; 
;; Permission is hereby granted, free of charge, to any person obtaining a copy
;; of this software and associated documentation files (the "Software"), to deal
;; in the Software without restriction, including without limitation the rights
;; to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
;; copies of the Software, and to permit persons to whom the Software is
;; furnished to do so, subject to the following conditions:
;; 
;; The above copyright notice and this permission notice shall be included in
;; all copies or substantial portions of the Software.
;; 
;; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
;; IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
;; FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
;; AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
;; LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
;; OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
;; THE SOFTWARE.

(require [pyherc.aspects [*]])
(require [pyherc.macros [*]])
(require [herculeum.ai.macros [*]])
(require [hy.extra.anaphoric [*]])
(import [pyherc.aspects [log-debug]]
        [herculeum.ai.basic [attack-enemy wait]]
        [pyherc.data [get-character get-location-tags]]
        [pyherc.data.geometry [area-around]]
        [pyherc.ports [perform-mitosis mitosis-legal? morph morph-legal?]]
        [random [choice]])

(setv __doc__ "module for AI routines for fungus")

(defclass FungusAI []
  
  [__doc__ "AI routine for fungus"
   character None]

  (defn --init-- [self character]
    "default constructor"
    (.--init-- (super FungusAI self))
    (setv self.character character))

  (defn act [self model action-factory rng]
    "check the situation and act accordingly"
    (fungus-act self model action-factory rng))

  (defn --call-- [self model action-factory rng]
    (. self act model action-factory rng)))

(defclass GreatFungusAI []

  [__doc__ "AI routine for great fungus"
   character None]

  (defn --init-- [self character]
    "default constructor"
    (.--init-- (super GreatFungusAI self))
    (setv self.character character))
  
  (defn act [self model action-factory rng]
    "check the situation and act accordingly"
    (great-fungus-act self model action-factory rng))

  (defn --call-- [self model action-factory rng]
    (. self act model action-factory rng)))


#d(defn fungus-act [ai model action-factory rng]
    (let [enemies (adjacent-enemies ai)]
      (if enemies
	(attack-enemy ai (choice enemies) action-factory rng)
        (rarely
         (cond [(and (mitosis-legal? ai.character)
                     (in "room" (get-location-tags ai.character.level
                                                   ai.character.location)))
                (perform-mitosis ai.character)]
               [(and (morph-legal? ai.character "great fungus")
                     (>= (count (adjacent-friends ai)) 6))
                (morph-great-fungi ai)]
               [True (wait ai)])
         (wait ai)))))

#d(defn great-fungus-act [ai model action-factory rng]
    (let [enemies (adjacent-enemies ai)]
      (if enemies
	(attack-enemy ai (choice enemies) action-factory rng)
        (wait ai))))

#d(defn morph-great-fungi [ai]
    "morph character into a great fungi"
    (morph ai.character "great fungus"
           (adjacent-friends ai)))

#d(defn adjacent-friends [ai]
    "get list of friends adjacent to given ai"
    (let [character ai.character
          level character.level
          location character.location
          characters (ap-map (get-character level it) (area-around location))]
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
    (let [loc ai.character.location
          level ai.character.level
          monsters []]
      (for [x (range (- (x-coordinate loc) 1) (+ (x-coordinate loc) 2))]
	(for [y (range (- (y-coordinate loc) 1) (+ (y-coordinate loc) 2))]
	  (let [creature (get-character level #t(x y))]
	    (when (and creature
		       (!= creature ai.character)
		       (!= creature.name ai.character.name))
	      (.append monsters creature)))))
      monsters))
