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
(require archimedes)
(require pyherc.macros)

(import [hamcrest [assert-that equal-to has-item is- is-not :as is-not-]]
        [mockito [mock verify any :as any-]]
        [pyherc.data [Dungeon cooldown add-character]]
        [pyherc.data.effects [Effect]]
        [pyherc.data.model [Model]]
        [pyherc.test.builders [CharacterBuilder EffectBuilder
                               RulesEngineBuilder LevelBuilder]])

(background characters
            [creature₁ (-> (CharacterBuilder)
                           (.with-tick 5)
                           (.with-speed 1)
                           (.with-name "creature 1")
                           (.build))]
            [creature₂ (-> (CharacterBuilder)
                           (.with-tick 0)
                           (.with-speed 2)
                           (.with-name "creature 2")
                           (.build))]
            [creature₃ (-> (CharacterBuilder)
                           (.with-tick 3)
                           (.with-speed 0.5)
                           (.with-name "creature 3")
                           (.build))]
             [model (Model)]
             [level (-> (LevelBuilder)
                        (.with-model model)
                        (.build))]
             [rules-engine (-> (RulesEngineBuilder)
                               (.build))]
             [_ (do (setv (. model dungeon) (Dungeon))
                    (setv (. model dungeon levels) level)
                    (cooldown creature₃ "shoryuken" 20)
                    (add-character level #t(5 5) creature₁)
                    (add-character level #t(6 6) creature₂)
                    (add-character level #t(7 7) creature₃)
                    (setv (. model player) creature₃))])

(fact "character whose tick is 0 is next in turn"
      (with-background characters [model creature₂ rules-engine]
        (assert-that (.get-next-creature model rules-engine)
                     (is- (equal-to creature₂)))))

(fact "when everyone has positive tick, the character with smallest tick is next in turn"
      (with-background characters [model rules-engine
                                   creature₁ creature₂ creature₃]
        (setv (. creature₁ tick) 5)
        (setv (. creature₂ tick) 10)
        (setv (. creature₃ tick) 3)
        (assert-that (.get-next-creature model rules-engine)
                     (is- (equal-to creature₃)))))

(fact "cooldowns of skills go down as time progresses"
      (with-background characters [model rules-engine 
                                   creature₁ creature₂ creature₃]
        (setv (. creature₁ tick) 50)
        (setv (. creature₂ tick) 100)
        (setv (. creature₃ tick) 30)
        (let [[creature (.get-next-creature model rules-engine)]]
          (assert-that (cooldown creature "shoryuken")
                      (is- (equal-to 0))))))

(background effects
            [creature (-> (CharacterBuilder)
                          (.with-tick 5)
                          (.build))]
            [long-effect (-> (EffectBuilder)
                             (.with-duration 50)
                             (.with-frequency 5)
                             (.with-tick 5)
                             (.with-effect-name "long effect")
                             (.build))]
            [short-effect (-> (EffectBuilder)
                              (.with-duration 5)
                              (.with-frequency 5)
                              (.with-tick 5)
                              (.with-effect-name "short effect")
                              (.build))]
            [model (Model)]
            [level (-> (LevelBuilder)
                       (.with-model model)
                       (.build))]
            [rules-engine (-> (RulesEngineBuilder)
                              (.build))]
            [_ (do (setv (. model player) creature)
                   (.add-effect creature short-effect)
                   (.add-effect creature long-effect)
                   (add-character level #t(5 5) creature))])

(fact "effect with zero tick will trigger"
      (with-background effects [creature model rules-engine]
        (let [[effect (mock Effect)]]
          (setv (. effect duration) 50)
          (setv (. effect frequency) 5)
          (setv (. effect tick ) 5)
          (.add-effect creature effect)
          (.get-next-creature model rules-engine)
          (-> (verify effect)
              (.trigger (any-))))))

(fact "tick of an effect will be reset after it has been triggered"
      (with-background effects [creature long-effect model rules-engine]
        (.get-next-creature model rules-engine)
        (assert-that (. long-effect tick)
                       (is- (equal-to 5)))))

(fact "effect duration goes down as time progresses"
      (with-background effects [creature long-effect model rules-engine]
        (.get-next-creature model rules-engine)
        (assert-that (. long-effect duration) (is- (equal-to 45)))))

(fact "expired effects are removed"
      (with-background effects [creature short-effect model rules-engine]
        (.get-next-creature model rules-engine)
        (assert-that (.get-effects creature) (is-not- (has-item short-effect)))))

(fact "only expired effects are removed, unexpired stay"
      (with-background effects [creature long-effect model rules-engine]
        (.get-next-creature model rules-engine)
        (assert-that (.get-effects creature) (has-item long-effect))))

(fact "all effects will have their timers decreased as time progresses"
      (let [[creature₁ (-> (CharacterBuilder)
                           (.with-tick 5)
                           (.build))]
            [model (Model)]
            [level (-> (LevelBuilder)
                       (.with-model model)
                       (.build))]
            [rules-engine (-> (RulesEngineBuilder)
                              (.build))]
            [effect₁ (-> (EffectBuilder)
                         (.with-duration 50)
                         (.with-frequency 5)
                         (.with-tick 5)
                         (.build))]
            [effect₂ (-> (EffectBuilder)
                         (.with-duration 50)
                         (.with-frequency 5)
                         (.with-tick 5)
                         (.build))]
            [creature₂ (-> (CharacterBuilder)
                           (.with-tick 10)
                           (.with-effect-handle effect₂)
                           (.build))]]
        (setv (. model player) creature₁)
        (add-character level #t(5 5) creature₁)
        (add-character level #t(6 6) creature₂)
        (.get-next-creature model rules-engine)
        (assert-that (. effect₁ tick)
                     (is- (equal-to (. effect₂ tick))))
        (setv (. creature₁ tick) 10)
        (.get-next-creature model rules-engine)
        (assert-that (. effect₁ tick)
                     (is- (equal-to (. effect₂ tick))))))
