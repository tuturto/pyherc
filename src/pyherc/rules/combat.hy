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

(require [hy.extra.anaphoric [ap-each ap-if]])
(require [hymn.dsl [*]])
(require [pyherc.macros [*]])
(require [pyherc.rules.macros [*]])

(import [hymn.types.either [Left Right right? left?]]
        [pyherc.data.constants [Duration]]
        [pyherc.data.damage [new-damage]]
        [pyherc.data.geometry [get-adjacent-target-in-direction
                               get-target-in-direction]]
        [pyherc.data.new-character [raise-event-m add-tick-m]]
        [pyherc.data.new-item [current-weapon current-ammunition]]
        [pyherc.data [get-character blocks-movement]]
        [pyherc.events [new-attack-hit-event new-attack-miss-event]])

(defn+ attack [character direction]
  "make given character to attack a direction"
  (if (call attack-legal? character direction)
    (do-monad-e [_ (attack-direction-m character direction)
                 _ (add-tick-m character (attack-duration character))]
                (Right character))
    (do-monad-e [_ add-tick-m character Duration.fast]
                (Left "attack was not legal"))))

(defn+ attack-legal? [character direction]
  "can this attack be done?"
  (is-not character None))

(defn attack-direction-m [character direction]
  "perform attack to direction, spend ammunition and check for dying"
  (ap-if (target-of-attack character direction)
         (do-monad-e [attack-type (attack-type-m character direction)
                      damage-list (damage-list-m character attack-type)
                      damage-result (apply-damage-list-m (. it target) damage-list)
                      _ (raise-attack-hit-m character
                                            attack-type
                                            (. it target)
                                            damage-result)
                      _ (handle-spending-ammunition-m character attack-type)
                      _ (trigger-attack-effects-m character (. it target))
                      _ (check-dying-m (. it target))]
                     (Right character))                      
         (do-monad-e [a₁ (raise-attack-nothing-m character)]
                     (Right character))))

(defn handle-spending-ammunition-m [character attack-type]
  "in case of ranged attack, use ammunition"
  (left-if-nil [character attack-type]
               (cond [(= "ranged" attack-type)
                      (do (setv ammo (current-ammunition character))
                          (setv (. ammo ammunition-data count)
                                (dec (. ammo ammunition-data count)))
                          (when (<= (. ammo ammunition-data count) 0)
                            (setv (. character inventory projectiles) None)
                            (.remove (. character inventory) ammo))                          
                          (Right character))]
                     [True (Right character)])))

(defn attack-type [character direction]
  (if (ranged-attack? character direction) "ranged"
      (melee-attack? character direction) "melee"
      "unarmed"))

(defn attack-type-m [character direction]
  (left-if-nil [character direction]
               (Right (attack-type character direction))))

(defn ranged-attack? [character direction]
  "will this be a ranged attack?"
  (let [weapon (current-weapon character)
        ammunition (current-ammunition character)
        next-square (.get-location-at-direction character direction)]    
    (if (not weapon) False
        (not ammunition) False
        (not (ammunition-types-match? weapon ammunition)) False
        (get-character character.level next-square) False
        (blocks-movement character.level next-square) False
        True)))

(defn melee-attack? [character direction]
  "will this be a melee attack?"
  (if (not (current-weapon character)) False
      (not (current-ammunition character)) True        
      True))

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

(defn damage-list-m [character attack-type]
  "get damage list of this character"
  (cond [(= "unarmed" attack-type) (Right [#t((.get-attack character)
                                              "crushing")])]
        [(= "melee" attack-type) (Right (. (current-weapon character)
                                           weapon-data damage))]
        [(= "ranged" attack-type) (Right (. (current-ammunition character)
                                            ammunition-data damage))]
        [True (Left (.format "attack type {0} is unknown" attack-type))]))

(defn apply-damage-list-m [character damage-list]
  (left-if-nil [character damage-list]
               (Right ((new-damage damage-list)
                       character))))

(defn target-of-attack [character direction]
  "locate target of given attack, if no target found, return nil"
  (if (ranged-attack? character direction)
    (get-target-in-direction (. character level)
                             (. character location)
                             direction)
    (get-adjacent-target-in-direction (. character level)
                                      (. character location)
                                      direction)))

(defn attack-duration [attacker]
  (ap-if (. attacker inventory weapon)
         (/ Duration.normal (. it weapon-data speed))
         Duration.normal))

(defn trigger-attack-effects-m [attacker target]
  (left-if-nil [attacker target]
               (let [weapon (. attacker inventory weapon)
                     effects (.get-effect-handles attacker "on attack hit")]
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
