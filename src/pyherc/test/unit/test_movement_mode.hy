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

(import [hamcrest [assert-that is- equal-to]])
(import [pyherc.data [movement-mode]]
        [pyherc.data.effects [MovementModeModifier]]
        [pyherc.test.builders [CharacterBuilder]])

(defn test-normal-movement-mode []
  "walk is default movement mode"
  (let [[character (-> (CharacterBuilder)
                       (.build))]]
    (assert-that (movement-mode character) (is- (equal-to "walk")))))

(defn test-flying-mode []
  "flying is reported as movement mode when it's only one"
  (let [[effect (MovementModeModifier :duration nil
                                      :frequency nil
                                      :tick nil
                                      :icon :icon
                                      :title "fly boosters"
                                      :description "internal fly boosters"
                                      :mode "fly")]
        [character (-> (CharacterBuilder)
                       (.with-effect effect)
                       (.build))]]
    (assert-that (movement-mode character) (is- (equal-to "fly")))))

(defn test-multiple-movement-mode-modifiers []
  "flying takes precedence over walking with movement modes"
  (let [[effect₁ (MovementModeModifier :duration nil
                                       :frequency nil
                                       :tick nil
                                       :icon :icon
                                       :title "fly boosters"
                                       :description "internal fly boosters"
                                       :mode "fly")]
        [effect₂ (MovementModeModifier :duration nil
                                       :frequency nil
                                       :tick nil
                                       :icon :icon
                                       :title "fly boosters"
                                       :description "internal fly boosters"
                                       :mode "walk")]
        [character (-> (CharacterBuilder)
                       (.with-effect effect₁)
                       (.with-effect effect₂)
                       (.build))]]
    (assert-that (movement-mode character) (is- (equal-to "fly")))))
