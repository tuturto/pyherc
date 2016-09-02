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

(require archimedes)
(require pyherc.macros)

(import [pyherc.data [add-character]]
        [pyherc.data.constants [Direction]]
        [pyherc.data.effects [MovementModeModifier]]
        [pyherc.test.builders [CharacterBuilder LevelBuilder]]
        [hamcrest [assert-that is- equal-to]]
        pyherc)

(defn flying []
  "create effect that allows character to fly"
  (MovementModeModifier :mode "fly"
                        :duration nil
                        :frequency nil
                        :tick 0
                        :icon nil
                        :title "flying"
                        :description "You feel like flying"))

(background default
            [action-factory (-> (ActionFactoryBuilder)
                                (.build))]
            [_ (set-action-factory action-factory)])

(fact "friendly characters can swap places when flying"
      (let [[level (-> (LevelBuilder)
                       (.build))]
            [character₀ (-> (CharacterBuilder)
                            (.with-effect (flying))                              
                            (.build))]
            [character₁ (-> (CharacterBuilder)
                            (.with-effect (flying))
                            (.build))]]
        (setv (. character₀ artificial-intelligence) (fn [] nil))
        (setv (. character₁ artificial-intelligence) (fn [] nil))
        (add-character level #t(5 5) character₀)
        (add-character level #t(6 5) character₁)
        (call move character₀ Direction.east)
        (assert-that (. character₀ location) (is- (equal-to #t(6 5))))
        (assert-that (. character₁ location) (is- (equal-to #t(5 5))))))
