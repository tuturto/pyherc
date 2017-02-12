;; -*- coding: utf-8 -*-

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

(import [pyherc.data.traps [PitTrap Caltrops]]
        [pyherc.generators [get-trap-creator]]
        [hamcrest [assert-that instance-of]])

(defn setup []
  "setup test case"
  (let [generator (get-trap-creator {"pit" [PitTrap {}]
                                           "caltrops" [Caltrops {"damage" 4}]})]
    {:generator generator}))

(defn test-creating-trap []
  "creation of a trap is possible with trap creator"
  (let [context (setup)
        generator (:generator context)
        trap (generator "pit")]
    (assert-that trap (instance-of PitTrap))))

(defn test-creating-trap-with-parameters []
  "creationg of trap with parameters is possible"
  (let [context (setup)
        generator (:generator context)
        trap (generator "caltrops")]
    (assert-that trap (instance-of Caltrops))))
