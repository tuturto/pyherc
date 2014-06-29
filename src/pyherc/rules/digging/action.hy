;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2014 Tuukka Turto
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

(require hy.contrib.anaphoric)
(require pyherc.aspects)
(require pyherc.macros)
(import [pyherc.aspects [log-debug]]
        [pyherc.data [area-around add-item add-character blocks-movement]]
        [pyherc.data.constants [Duration]]
        [pyherc.data.features [clear-cache feature-level feature-location
                               items-in-cache characters-in-cache]]
        [pyherc.events [DigEvent]])

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
                    (.raise-event self.character (DigEvent self.character
                                                           cache items
                                                           characters)))))]])

(defn using-spade? [character]
  "check if this character is currently using a spade"
  (let [[weapon character.inventory.weapon]]
    (if (= weapon nil) false
        (if (in :spade weapon.tags) true false))))

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
