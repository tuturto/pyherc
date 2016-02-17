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
(require archimedes)

(import [hamcrest [assert-that is- equal-to less-than]]
        [random]
        [pyherc.test.builders [ActionFactoryBuilder CharacterBuilder
                               LevelBuilder]]
        [pyherc.ports [set-action-factory lunge]]
        [pyherc.data [add-character]]
        [pyherc.data.constants [Direction]])

(background default            
            [character₀ (-> (CharacterBuilder)
                            (.build))]
            [character₁ (-> (CharacterBuilder)
                            (.build))]
            [level (-> (LevelBuilder)
                       (.build))]
            [_ (set-action-factory (-> (ActionFactoryBuilder)
                                       (.with-attack-factory)
                                       (.with-move-factory)
                                       (.build)))])

(fact "unarmed lunge moves attacker"
      (with-background default [character₀ character₁ level]
        (add-character level #t(5 5) character₀)
        (add-character level #t(5 7) character₁)
        (lunge character₁ Direction.north random)
        (assert-that character₁.location (is- (equal-to #t(5 6))))))

(fact "unarmed lunge damages target"
  (with-background default [character₀ character₁ level]
    (let [[old-hp (. character₀ hit-points)]]
      (add-character level #t(5 5) character₀)
      (add-character level #t(5 7) character₁)
      (lunge character₁ Direction.north random)
      (assert-that character₀.hit-points (is- (less-than old-hp))))))

(fact "lunging against opponent right next to attacker is not possible"
      (with-background default [character₀ character₁ level]
        (let [[old-hp (. character₀ hit-points)]]
          (add-character level #t(5 5) character₀)
          (add-character level #t(5 6) character₁)
          (lunge character₁ Direction.north random)
          (assert-that character₁.location (is- (equal-to #t(5 6))))
          (assert-that character₀.hit-points (is- (equal-to old-hp))))))
