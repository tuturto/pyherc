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
(require pyherc.rules.macros)

(import [pyherc.rules.public [ActionParameters]]
        [pyherc.ports [interface]])

(defn cast [character direction spell-name]
  "cast a spell"
  (run-action (SpellCastingParameters character
                                      direction
                                      spell-name)))

(defn casting-legal? []
  (legal-action? (SpellCastingParameters character
                                         direction
                                         spell-name)))

(defn gain-domain [character domain item]
  "sacrifice an item to gain a domain"
  (run-action (GainDomainParameters character domain item)))

(defn gaining-domain-legal? []
  (legal-action? (GainDomainParameters character domain item)))

(defclass SpellCastingParameters [ActionParameters]
  [[--init-- (fn [self caster direction spell-name]
               (super-init "spell casting")
               (set-attributes caster direction spell-name)
               nil)]])

(defclass GainDomainParameters [ActionParameters]
  [[--init-- (fn [self character item domain]
               (super-init "gain domain")
               (set-attributes character item domain)
               (setv self.action-type "gain domain")
               nil)]])
