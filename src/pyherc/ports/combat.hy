;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2015 Tuukka Turto
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

(require pyherc.macros)
(require pyherc.rules.macros)

(import [pyherc.data [current-weapon current-ammunition get-character
                      blocks-movement]]
        [pyherc.rules.public [ActionParameters]]
        [pyherc.ports [interface]])

(defn attack [character direction rng]
  "attack to given direction"
  (run-action (AttackParameters character
                                direction
                                (attack-type character direction)
                                rng)))

(defn attack-legal? [character direction]
  (legal-action? (AttackParameters character
                                   direction
                                   (attack-type character direction)
                                   rng))) 

(defparams AttackParameters
  "attack"
  [attacker direction attack-type rng])

(defn attack-type [character direction]
  (cond [(ranged-attack? character direction) "ranged"]
        [(melee-attack? character direction) "melee"]
        [true "unarmed"]))

(defn ranged-attack? [character direction]
  "will this be a ranged attack?"
  (let [[weapon (current-weapon character)]
        [ammunition (current-ammunition character)]
        [next-square (.get-location-at-direction character direction)]]    
    (cond [(not weapon) false]
          [(not ammunition) false]
          [(not (ammunition-types-match? weapon ammunition)) false]
          [(get-character character.level next-square) false]
          [(blocks-movement character.level next-square) false]
          [true true])))

(defn melee-attack? [character direction]
  "will this be a melee attack?"
  (cond [(not (current-weapon character)) false]
        [(not (current-ammunition character)) true]        
        [true true]))

(defn ammunition-types-match? [weapon ammunition]
  "do weapon and ammunition match?"
  (and weapon ammunition
       weapon.weapon-data
       ammunition.ammunition-data
       (= weapon.weapon-data.ammunition-type
          ammunition.ammunition-data.ammunition-type)))
