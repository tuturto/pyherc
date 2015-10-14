;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2015 Tuukka Turto
;;
;;   This file is part of pyherc.
;;
;;   pyherc is free software: you can redistribute it and/or modify
;;   it under the terms of the GNU General Public License as published by
;;   the Free Software Foundation, either version 3 of the License, or
;;   (at your option) any later version.
;;
;;   pyherc is distributed in the hope that it will be useful,
;;   but WITHOUT ANY WARRANTY; without even the implied warranty of
;;   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;   GNU General Public License for more details.
;;
;;   You should have received a copy of the GNU General Public License
;;   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

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
