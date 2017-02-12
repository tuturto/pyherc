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

(require [archimedes [fact background with-background]])

(import [hamcrest [assert-that is- equal-to]]
        [pyherc.data.constants [sizes]]
        [pyherc.data.new-character [size smaller? larger? same-size?
                                    different-size?]]
        [pyherc.test.builders [CharacterBuilder]])

(background default
            character (-> (CharacterBuilder)
                          (.build)))

(fact "setting and retrieving character size is possible"
      (with-background default [character]
        (size character 'tiny)
        (assert-that (size character) (is- (equal-to 'tiny)))))

(fact "tiny is smaller than small"
      (assert-that (smaller? 'tiny 'small) (is- (equal-to True))))

(fact "large is not smaller than small"
      (assert-that (smaller? 'large 'small) (is- (equal-to False))))

(fact "medium is larger than small"
      (assert-that (larger? 'medium 'small) (is- (equal-to True))))

(fact "large is not larger than huge"
      (assert-that (larger? 'large 'huge) (is- (equal-to False))))

(fact "huge is same size as huge"
      (assert-that (same-size? 'huge 'huge) (is- (equal-to True))))

(fact "small is not same size as huge"
      (assert-that (same-size? 'small 'huge) (is- (equal-to False))))

(fact "medium is different size as large"
      (assert-that (different-size? 'medium 'large) (is- (equal-to True))))

(fact "tiny is not different size as tiny"
      (assert-that (different-size? 'tiny 'tiny) (is- (equal-to False))))
