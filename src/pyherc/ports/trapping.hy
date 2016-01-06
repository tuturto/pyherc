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
(import [pyherc.rules.public [ActionParameters]]
        [pyherc.ports [interface]])

(defn place-trap [character trap-bag]
  "place trap"
  (let [[action (.get-action interface.*factory*
                             (TrappingParameters character :trap-bag trap-bag))]]
    (when (.legal? action)
      (.execute action))))

(defn place-natural-trap [character trap-name]
  "place trap without using any items"
  (let [[action (.get-action interface.*factory*
                             (TrappingParameters character :trap-name trap-name))]]
    (when (.legal? action)
      (.execute action))))

(defn trapping-legal? [character trap-bag]
  "check if character can place a trap"
  (let [[action (.get-action interface.*factory*
                             (TrappingParameters character :trap-bag trap-bag))]]
    (.legal? action)))

(defn natural-trapping-legal? [character trap-name]
  "check if character can place a natural trap"
  (let [[action (.get-action interface.*factory*
                             (TrappingParameters character :trap-name trap-name))]]
    (.legal? action)))

(defclass TrappingParameters [ActionParameters]
  "class controlling creation of TrappingAction"
  [[--init-- (fn [self character &optional [trap-bag nil] [trap-name nil]]
               (super-init)
               (set-attributes character trap-bag trap-name)
               (setv self.action-type "trapping")
               nil)]])
