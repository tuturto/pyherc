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

(require pyherc.aspects)
(require pyherc.macros) ;; TODO: remove this if xor ever lands Hy

(import [hymn.types.either [Left Right]]
        [pyherc.aspects [log-debug]]
        [pyherc.data [add-trap trap-bag?]]
        [pyherc.data.constants [Duration]]
        [pyherc.events [new-trap-placed-event]])

(defclass TrappingAction []
  "Action of placing a trap"
  [[--init-- #d(fn [self character trap-bag trap-name trap-creator]
                 "default constructor"
                 (super-init)
                 (assert character)
                 (assert (xor trap-bag trap-name))
                 (assert trap-creator)
                 (setv self.character character)
                 (setv self.trap-bag trap-bag)
                 (setv self.trap-name trap-name)
                 (setv self.trap-creator trap-creator)
                 nil)]
   [legal? #d(fn [self]
               "check if action is possible to perform"
               (if self.trap-bag
                 (and (in self.trap-bag self.character.inventory)
                      (trap-bag? self.trap-bag))
                 true))]
   [execute #d(fn [self]
                "execute the action"
                (if (.legal? self)
                  (let [[character self.character]
                        [level character.level]
                        [location character.location]
                        [trap (get-trap self.trap-creator
                                        self.trap-bag
                                        self.trap-name)]]
                    (add-trap level location trap)
                    (.raise-event character (new-trap-placed-event character
                                                                   trap))
                    (when self.trap-bag
                      (setv self.trap-bag.trap-data.count 
                            (dec self.trap-bag.trap-data.count))
                      (when (< self.trap-bag.trap-data.count 1)
                        (character.inventory.remove self.trap-bag)))
                    (.add-to-tick character Duration.normal)
                    (Right self.character))
                  (Left self.character)))]])

(defn get-trap [trap-creator trap-bag trap-name]
  "get trap instance"
  (if trap-bag
    (trap-creator trap-bag.trap-data.trap-name)
    (trap-creator trap-name)))
