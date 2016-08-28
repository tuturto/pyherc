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

(require hy.contrib.anaphoric)
(require hymn.dsl)
(require pyherc.macros)
(require pyherc.rules.macros)

(import [hymn.types.either [Left Right right? left?]]
        [pyherc.data.constants [Duration]]
        [pyherc.data.damage [new-damage]]
        [pyherc.data.geometry [get-adjacent-target-in-direction]]
        [pyherc.data.new-character [raise-event-m add-tick-m]]
        [pyherc.data.new-item [current-weapon current-ammunition]]
        [pyherc.data [get-character blocks-movement]]
        [pyherc.events [new-attack-hit-event new-attack-miss-event]])

(defn+ attack [character direction]
  "make given character to attack a direction"
  (if (call attack-legal? character direction)
    (ap-if (target-of-attack character direction)   ;; in ranged attack, this should be something else?
           (do-monad-e [attack-type (attack-type-m character direction)
                        damage-list (damage-list-m character)
                        damage-result (apply-damage-list-m (. it target) damage-list)
                        a₁ (raise-attack-hit-m character
                                               attack-type
                                               (. it target)
                                               damage-result)
                        a₂ (trigger-attack-effects-m character (. it target))
                        a₃ (check-dying-m (. it target))
                        a₄ (add-tick-m character (attack-duration character))]
                       (Right character))                      
           (do-monad-e [a₁ (raise-attack-nothing-m character)]
                       (Right character)))
    (do-monad-e [a₁ add-tick-m character (/ Duration.fast (speed-modifier character))]
                (Left "attack was not legal"))))

(defn+ attack-legal? [character direction]
  "can this attack be done?"
  (is-not character nil))

(defn attack-type-m [character direction]
  (left-if-nil [character direction]
               (cond [(ranged-attack? character direction) (Right "ranged")]
                     [(melee-attack? character direction) (Right "melee")]
                     [true (Right "unarmed")])))

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

(defn check-dying-m [character]
  "check if character should die"
  (left-if-nil [character]
               (Right (call check-dying character))))

(defn damage-list-m [character]
  "get damage list of this character"
  (ap-if (current-weapon character)
         (Right (. it weapon-data damage))
         (Right [#t((.get-attack character) "crushing")])))

(defn apply-damage-list-m [character damage-list]
  (left-if-nil [character damage-list]
               (Right ((new-damage damage-list)
                       character))))

(defn target-of-attack [character direction] ;;TODO: ranged combat
  "locate target of given attack, if no target found, return nil"
  (get-adjacent-target-in-direction (. character level)
                                    (. character location)
                                    direction))

(defn attack-duration [attacker]
  (ap-if (. attacker inventory weapon)
         (/ Duration.normal (. it weapon-data speed))
         Duration.normal))

(defn trigger-attack-effects-m [attacker target]
  (left-if-nil [attacker target]
               (let [[weapon (. attacker inventory weapon)]
                     [effects (.get-effect-handles attacker "on attack hit")]]
                 (when weapon
                   (.extend effects (.get-effect-handles weapon "on attack hit")))
                 (ap-each effects
                          (setv effect (call create-effect (. it effect) :target target))
                          (if (or (not effect)
                                  (<= (. effect duration) 0))
                            (.trigger effect)
                            (.add-effect target effect)))
                 (Right attacker))))

(defn raise-attack-nothing-m [attacker]
  (left-if-nil [attacker]
               (raise-event-m attacker
                              (new-attack-nothing-event :attacker attacker))
               (Right attacker)))

(defn raise-attack-hit-m [attacker attack-type target damage-caused]
  (left-if-nil [attacker attack-type target damage-caused]
               (raise-event-m attacker
                              (new-attack-hit-event :type attack-type
                                                    :attacker attacker
                                                    :target target
                                                    :damage damage-caused))
               (Right attacker)))

(defn raise-attack-miss-m [attacker attack-type target]
  (left-if-nil [attacker attack-type target]
               (raise-event-m attacker
                              (new-attack-miss-event :type attack-type
                                                     :attacker attacker
                                                     :target target))
               (Right attacker)))
