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

(require [pyherc.rules.macros [*]])

(date-rules
 (christmas (= month 12) (in day [24 25 26]))
 (aprilfools (= month 4) (= day 1))
 (babbage-born (= month 12) (= day 26))
 (babbage-died (= month 10) (= day 18))
 (gödel-born (= month 4) (= day 28))
 (gödel-died (= month 1) (= day 14))
 (jacquard-born (= month 7) (= day 7))
 (jacquard-died (= month 8) (= day 7))
 (lovelace-born (= month 12) (= day 10))
 (lovelace-died (= month 11) (= day 27))
 (turing-born (= month 6) (= day 23))
 (turing-died (= month 6) (= day 7)))
