;; -*- coding: utf-8 -*-

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

(require pyherc.config.dsl.traps)
(require herculeum.config.levels.macros)

(items-dsl)
(traps-dsl)

(traps ("pit" PitTrap)
       ("small caltrops" Caltrops "damage" 1 "icon" "caltrops")
       ("large caltrops" Caltrops "damage" 2 "icon" "caltrops"))

(items-list
 (trap-bag "bag of small caltrops"
           "a small bag filled with sharp caltrops"
           "small caltrops"
           1 150 1 ["bag"] ["trap bag"] "common")
 (trap-bag "greater bag of caltrops"
           "a rather large bag filled with sharp caltrops"
           "small caltrops"
           3 450 1 ["bag"] ["trap bag"] "uncommon")
 (trap-bag "bag of brutal caltrops"
           "a small bag of rather nasty looking caltrops"
           "large caltrops"
           1 250 1 ["bag"] ["trap bag"] "uncommon"))
