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

(require [pyherc.macros [*]])
(require [hymn.dsl [*]])

(import [hymn.types.either [Right Left left?]]
        [pyherc.data [skill-ready? cooldown free-passage get-characters]]
        [pyherc.data.constants [Duration]]
        [pyherc.data.new-character [add-tick-m cooldown-m]]
        [pyherc.rules.moving [move-character-to-location-m trigger-traps-m]]
        [pyherc.rules.combat [attack-duration attack-type attack-direction-m]]
        [pyherc])

(defn+ lunge [character direction]
  "quickly jump forward and perform melee attack"
  (if (call lunge-legal? character direction)
    (do-monad-e [_ (jump-forward-m character direction)
                 _ (if (> (. character hit-points) 0)
                     (attack-m character direction)
                     (Right character))]
                (Right character))
    (do-monad-e [_ (add-tick-m character Duration.fast)]
                (Left "lunge wasn't legal"))))

(defn jump-forward-m [character direction]
  (left-if-nil [character direction]
               (do-monad-e [_ (move-character-to-location-m character
                                                            (.get-location-at-direction character direction)
                                                            (. character level))
                            _ (add-tick-m character Duration.instant)
                            _ (trigger-traps-m character)]
                           (Right character))))

(defn attack-m [character direction]
  (left-if-nil [character direction]
               (do-monad-e [_ (attack-direction-m character direction)
                            _ (cooldown-m character "lunge" Duration.very-slow)
                            _ (add-tick-m character (attack-duration character))]
                           (Right character))))

(defn+ lunge-legal? [character direction]
  "is it legal to start lunge attack"
  (let [new-location (.get-location-at-direction character direction)]
    (and (skill-ready? character "lunge")
         (free-passage (. character level) new-location)
         (not (get-characters (. character level) new-location))
         (in (attack-type character direction) ["melee" "unarmed"]))))
