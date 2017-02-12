;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2017 Tuukka Turto
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

(import [pyherc.generators [ItemConfiguration TrapConfiguration]])

(defmacro items-dsl []
  `(import [herculeum.config.levels.macros [item tome scroll rare-scroll
                                            artifact-scroll trap-bag]]))

(defn item [name description cost weight icons types rarity]  
  (ItemConfiguration :name name
                     :cost cost
                     :weight weight
                     :icons icons
                     :types types
                     :rarity rarity
                     :description description))

(defmacro def-scroll [name cost rarity]
  `(defn ~name [name &rest content]
     (item name (.join " " content) ~cost 1
           ["tied-scroll"] ["scroll" "hint"]
           ~rarity)))

(defn tome [name &rest content]
  (item name (.join " " content) 100 1
        ["tied-scroll"] ["tome" "hint"]
        "rare"))

(def-scroll scroll 50 "uncommon")
(def-scroll rare-scroll 100 "rare")
(def-scroll artifact-scroll 750 "artifact")

(defn trap-bag [name description trap-name count cost weight icons types rarity]
  (ItemConfiguration :name name
                     :cost cost
                     :weight weight
                     :icons icons
                     :types types
                     :rarity rarity
                     :trap-configuration (TrapConfiguration trap-name count)
                     :description description))

(defmacro items-list [&rest items]
  `(defn init-items [context]
     [~@items]))
