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

(import [pyherc.events [new-effect-added-event new-effect-removed-event]])

(require pyherc.macros)

(defclass Effect []
  "class representing effects"
  [[--init-- (fn [self duration frequency tick icon title description]
               "default initializer"
               (super-init)
               (set-attributes duration frequency tick icon title description)
               (setv self.effect-name "effect")
               (setv self.multiple-allowed false)
               nil)]
   [trigger (fn [self dying-rules]
              "trigger the effect"
              (.do-trigger self dying-rules)
              (.post-trigger self))]
   [do-trigger (fn [self dying-rules]
                 "override this method to contain logic of the effect"
                 nil)]
   [post-trigger (fn [self]
                   "do house keeping after effect has been triggered"
                   (when (is-not self.duration nil)
                     (setv self.tick self.frequency)
                     (setv self.duration (- self.duration self.frequency))))]
   [get-add-event (fn [self]
                    "get event describing adding this effect"
                    (new-effect-added-event self))]
   [get-removal-event (fn [self]
                        "get event describing removing this effect"
                        (new-effect-removed-event self))]])

(defclass EffectHandle []
  "handle that can be used to construct effects"
  [[--init-- (fn [self trigger effect parameters charges]
               "default initializer"
               (super-init)
               (set-attributes trigger effect parameters charges)
               nil)]
   [--str-- (fn [self]
              "string representation of this object"
              (.format "trigger: {0}, effect: {1}, parameters: {2}, charges: {3}"
                       self.trigger self.effect self.parameters self.charges))]])
