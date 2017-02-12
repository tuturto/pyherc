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

(import [pyherc.data.damage [new-damage]]
        [pyherc.data.traps.trap [Trap]]
        [pyherc.data [get-traps remove-trap Duration]]
        [pyherc.events [damage-triggered damage-trap-triggered]])

(defclass Caltrops [Trap]
  [--init-- (fn [self damage &optional [icon None]]
              (super-init icon)
              (setv self.damage damage))
   on-enter (fn [self character]
              (let [damage (new-damage #t(#t(self.damage "piercing")))
                    total-damage (damage :target character
                                         :body-part "feet")]
                (.raise-event character (damage-trap-triggered character
                                                               self
                                                               total-damage))
                (.add-to-tick character Duration.slow)))
   on-place (fn [self level location]
              (let [traps (list-comp x [x (get-traps level location)]
                                     (isinstance x Caltrops))]
                (when (>= (len traps) 2)
                  (remove-trap level self))))])
