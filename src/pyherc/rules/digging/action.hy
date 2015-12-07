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
(import [pyherc.aspects [log-debug]]
        [pyherc.data [area-around add-item add-character blocks-movement]]
        [pyherc.data.constants [Duration]]
        [pyherc.data.features [clear-cache feature-level feature-location
                               items-in-cache characters-in-cache]]
        [pyherc.events [new-dig-event]])

(defclass DigAction []
  [[--init-- #d(fn [self character cache rng]
                 "default constructor"
                 (-> (super) (.--init--))
                 (setv self.character character)
                 (setv self.cache cache)
                 (setv self.rng rng)
                 nil)]
   [legal? #d(fn [self]
               "check if action is possible to perform"
               (when self.cache
                 (using-spade? self.character)))]
   [execute #d(fn [self]
                "execute the action"
                (when (.legal? self)
                  (let [[level (feature-level self.cache)]
                        [location (feature-location self.cache)]
                        [cache self.cache]
                        [items (list (items-in-cache cache))]
                        [characters (list (characters-in-cache cache))]]
                    (.add-to-tick self.character Duration.very-slow)
                    (distribute-items level location items self.rng)
                    (distribute-characters level location characters self.rng)
                    (clear-cache self.cache)
                    (.raise-event self.character (new-dig-event self.character
                                                                cache items
                                                                characters)))))]])

(defn using-spade? [character]
  "check if this character is currently using a spade"
  (let [[weapon character.inventory.weapon]]
    (if (= weapon nil) false
        (if (in "spade" weapon.tags) true false))))

(defn distribute-items [level location items rng]
  "distribute items around given spot"
  (ap-each items (add-item level
                           (free-location level location rng)
                           it)))

(defn distribute-characters [level location characters rng]
  "distribute characters around given spot"
  (ap-each characters (do
                       (.add-to-tick it Duration.very-slow)
                       (add-character level
                                      (free-location level location rng)
                                      it))))

(defn free-location [level location rng]
  "find a free location around given spot"
  (let [[free-spots (list-comp loc [loc (area-around location)]
                               (not (blocks-movement level loc)))]]
    (when free-spots (.choice rng free-spots))))
