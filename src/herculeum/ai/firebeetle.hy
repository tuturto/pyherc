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

(setv __doc__ "module for AI routines for firebeetles")

(require pyherc.macros)
(import [herculeum.ai.patrol [patrol-ai]]
        [pyherc.data [open-area?]])

(defclass FireBeetleAI []
  [[__doc__ "AI routine for fire beetles"]
   [character None]
   [mode ["transit" None]]
   [--init-- (fn [self character]
           "default constructor"
           (.--init-- (super FireBeetleAI self))
           (setv self.character character) None)]
   [act (fn [self model action-factory rng]
      "check the situation and act accordingly"
      (beetle-act self model action-factory))]
   [--call-- (fn [self model action-factory rng]
               (. self act model action-factory rng))]])

(def beetle-act (patrol-ai open-area? 3))
