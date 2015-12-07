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
(import [pyherc.rules.trapping.action [TrappingAction]])
(import [pyherc.aspects [log-debug log-info]])

(defclass TrappingFactory []
  "factory for creating trapping actions"
  [[--init-- #i(fn [self trap-creator]
                 (-> (super) (.--init--))
                 (setv self.action-type "trapping")
                 (setv self.trap-creator trap-creator)
                 nil)]
   [can-handle #d(fn [self parameters]
                   "can this factory handle a given action"
                   (= self.action-type parameters.action-type))]
   [get-action #d(fn [self parameters]
                   "create trapping action"
                   (TrappingAction parameters.character
                                   :trap-name parameters.trap-name
                                   :trap-bag parameters.trap-bag
                                   :trap-creator self.trap-creator))]])
