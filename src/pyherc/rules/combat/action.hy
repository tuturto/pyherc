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
(require pyherc.aspects)
(require pyherc.rules.macros)
(require hymn.dsl)
(require hy.contrib.anaphoric)

(import [hymn.types.either [Left Right]]
        [pyherc.aspects [log-debug log-info]]
        [pyherc.data.constants [Duration]]
        [pyherc.data.damage [new-damage]]
        [pyherc.events [new-attack-hit-event new-attack-miss-event
                        new-attack-nothing-event]]
        [random [Random]]
        [pyherc])

(action-dsl)

(defaction attack "action for attacking"
  :parameters [attack-type to-hit damage attacker target effect-factory additional-rules]

  :legal-action (let [[target (. self target target)]]
                  (if (is target nil)
                    (raise-attack-nothing (. self attacker))
                    (do (if (self.to-hit.hit?)
                          (do (raise-attack-hit (. self attacker)
                                                (. self attack-type)
                                                target
                                                (self.damage target))
                              (trigger-attack-effects (. self attacker) target (. self effect-factory))
                              (call check-dying target))
                          (raise-attack-miss (. self attacker)
                                             (. self attack-type)
                                             target))                        
                        (self.additional-rules.after-attack)
                        (.add-to-tick (. self attacker) (attack-duration (. self attacker)))))
                  (Right (. self attacker)))
  
  :illegal-action (Left (. self attacker))
  
  :legal? (not (is (. self attacker) nil))
  
  :to-string (.format "{0} attacking with {1}"
                      (. self attacker)
                      (. self attack-type)))

(defn attack-duration [attacker]
  (ap-if (. attacker inventory weapon)
         (/ Duration.normal (. it weapon-data speed))
         Duration.normal))

(defn trigger-attack-effects [attacker target factory]
  (let [[weapon (. attacker inventory weapon)]
        [effects (.get-effect-handles attacker "on attack hit")]]
    (when weapon
      (.extend effects (.get-effect-handles weapon "on attack hit")))
    (ap-each effects
             (setv effect (factory (. it effect) :target target))
             (if (or (not effect)
                     (<= (. effect duration) 0))
               (.trigger effect)
               (.add-effect target effect)))))

(defn raise-attack-nothing [attacker]
  (.raise-event attacker
                (new-attack-nothing-event :attacker attacker)))

(defn raise-attack-hit [attacker attack-type target damage-caused]
  (.raise-event attacker
                (new-attack-hit-event :type attack-type
                                      :attacker attacker
                                      :target target
                                      :damage damage-caused)))

(defn raise-attack-miss [attacker attack-type target]
  (.raise-event attacker
                (new-attack-miss-event :type attack-type
                                       :attacker attacker
                                       :target target)))

(defclass ToHit []
  [[--init-- (fn [self attacker target]
               "default initializer"
               (set-attributes attacker target)
               (setv self.rng (Random))
               nil)]
   [hit? (fn [self]
           true)]])

(defclass AdditionalRules []
  [[--init-- (fn [self attacker]
               nil)]
   [after-attack (fn [self]
                   nil)]])
