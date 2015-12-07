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


(require hy.contrib.anaphoric)
(require pyherc.aspects)
(require pyherc.macros)

(import [pyherc.aspects [log-debug log-info]]
        [pyherc.data [location-features get-tile]]
        [pyherc.data.features [feature-type]]
        [pyherc.rules.digging.action [DigAction]])

(defclass DigFactory []
  [[--init-- #i(fn [self rng]
                 "default constructor"
                 (-> (super) (.--init--))
                 (setv self.action-type "dig")
                 (setv self.rng rng)
                 nil)]
   [can-handle #d(fn [self parameters]
                   "can this factory handle a given action"
                   (= self.action-type parameters.action-type))]
   [get-action #d(fn [self parameters]
                   "create digging action"
                   (let [[character parameters.character]
                         [location character.location]
                         [level character.level]
                         [cache (get-cache level location)]]
                     (DigAction character cache self.rng)))]])

(defn get-cache [level location]
  (let [[caches (list-comp feature 
                           [feature (location-features level location)]
                           (= (feature-type feature) "cache"))]]
    (when (> (len caches) 0)
      (first caches))))
