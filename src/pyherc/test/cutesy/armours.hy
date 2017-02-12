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

(require [pyherc.test.cutesy.macros [*]])

(import [pyherc.data.effects [MovementModeModifier]]
        [pyherc.test.builders [ItemBuilder]])

(item LeatherArmour
      (.with-name "leather armour")
      (.with-damage-reduction 1)
      (.with-speed-modifier 1.0))

(item ScaleMail
      (.with-name "scale mail")
      (.with-damage-reduction 3)
      (.with-speed-modifier 0.7))

(item PlateMail
      (.with-name "plate mail")
      (.with-damage-reduction 5)
      (.with-speed-modifier 0.5))

(item LightBoots
      (.with-name "light boots")
      (.with-boots-damage-reduction 1)
      (.with-boots-speed-modifier 0.9))

(item HeavyBoots
      (.with-name "heavy boots")
      (.with-boots-damage-reduction 3)
      (.with-boots-speed-modifier 0.8))

(item IronBoots
      (.with-name "iron boots")
      (.with-boots-damage-reduction 4)
      (.with-boots-speed-modifier 0.75))

(item SpeedBoots
      (.with-name "speed boots")
      (.with-boots-damage-reduction 1)
      (.with-boots-speed-modifier 1.2))

(item FlyingBoots
      (.with-name "flying boots")
      (.with-boots-damage-reduction 1)
      (.with-boots-speed-modifier 1)
      (.with-effect (MovementModeModifier :duration None
                                          :frequency None
                                          :tick None
                                          :icon :icon
                                          :title "fly boosters"
                                          :description "internal fly boosters"
                                          :mode "fly")))
