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

(import [pyherc.test.builders [CharacterBuilder]]
        [hamcrest [assert-that is- equal-to]]
        [pyherc.data [skill-ready?]])

(defn test-zero-cooldown []
  "a skill with zero cool down is ready to be used"
  (let [[character (-> (CharacterBuilder)
                       (.with-cooldown "shoryuken" 0)
                       (.build))]]
    (assert-that (skill-ready? character "shoryuken")
                 (is- (equal-to true)))))

(defn test-non-zero-cooldown []
  "a skill with non-zero cool down is not ready to be used"
  (let [[character (-> (CharacterBuilder)
                       (.with-cooldown "shoryuken" 200)
                       (.build))]]
    (assert-that (skill-ready? character "shoryuken")
                 (is- (equal-to false)))))
