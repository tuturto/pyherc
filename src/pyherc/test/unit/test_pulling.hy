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

(require [pyherc.macros [*]])
(require [archimedes [*]])

(import [pyherc]
        [pyherc.data.level [add-character]]
        [pyherc.test.builders [CharacterBuilder LevelBuilder]]
        [hamcrest [assert-that is- equal-to]])

(background default
            medium-character (-> (CharacterBuilder)
                                 (.with-size 'medium)
                                 (.build)) 
            tiny-character (-> (CharacterBuilder)
                               (.with-size 'tiny)
                               (.build)))

(fact "character can pull target smaller than itself"
      (with-background default [medium-character tiny-character]
        (assert-that (call can-pull? medium-character tiny-character)
                     (is- (equal-to True)))))

(fact "character can not pull target larger than itself"
      (with-background default [medium-character tiny-character]
        (assert-that (call can-pull? tiny-character medium-character)
                     (is- (equal-to False)))))
