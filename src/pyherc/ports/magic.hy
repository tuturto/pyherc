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

(defn cast [character direction spell-name]
  "cast a spell"
  (let [[action (.get-action interface.*factory*
                             (SpellCastingParameters character
                                                     direction
                                                     spell-name))]]
    (when (.legal? action)
      (.execute action))))

(defn casting-legal? []
  true) ;; TODO: implement

(defn gain-domain [character domain item]
  "sacrifice an item to gain a domain"
  (let [[action (.get-action interface.*factory*
                             (GainDomainParameters character domain item))]]
    (when (.legal? action)
      (.execute action))))

(defn gaining-domain-legal? []
  true) ;; TODO: implement

(defclass SpellCastingParameters [ActionParameters]
  [[--init-- (fn [self caster direction spell-name]
               (super-init)
               (set-attributes caster direction spell-name)
               (setv self.action-type "spell casting")
               nil)]])

(defclass GainDomainParameters [ActionParameters]
  [[--init-- (fn [self character item domain]
               (super-init)
               (set-attributes character item domain)
               (setv self.action-type "gain domain")
               nil)]])
