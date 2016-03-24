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

(require archimedes)
(require pyherc.macros)

(import [hamcrest [assert-that is-not :as is-not- is- equal-to
                   has-length has-items]]
        [hypothesis.strategies [integers]]
        [pyherc.markov [chain-factory]])

(background infinite-foo-chain
            [factory (chain-factory :start-elements [#t("foo" 1 100)]
                                    :elements {"foo" [#t("foo" 1 100)]})]
            [chain (factory)])

(fact "first element of chain can be read"
      (with-background infinite-foo-chain [chain]
        (assert-that (first chain) (is- (equal-to "foo")))))

(fact "taking n elements from infinite chain will not exhaust it"
      (variants :n (integers :min-value 2))
      (with-background infinite-foo-chain [chain]
        (drop n chain)
        (assert-that (first chain) (is- (equal-to "foo")))))

(background one-element-chain
            [factory (chain-factory :start-elements [#t("foo" 1 100)]
                                    :elements {"foo" []})]
            [chain (factory)])

(fact "one element markov chain contains only one element"
      (variants :n (integers :min-value 1))
      (example :n 1)
      (with-background one-element-chain [chain]
        (assert-that (list (take 10 chain))
                     (has-length 1))))

(background flip-flop-chain
            [factory (chain-factory :start-elements [#t("flip" 1 100)]
                                    :elements {"flip" [#t("flop" 1 100)]
                                               "flop" [#t("flip" 1 100)]})]
            [chain (factory)])

(fact "markov chain can switch between states"
      (with-background flip-flop-chain [chain]
        (assert-that (first chain) (is- (equal-to "flip")))
        (assert-that (first chain) (is- (equal-to "flop")))
        (assert-that (first chain) (is- (equal-to "flip")))))

(background foo-bar-baz
            [factory (chain-factory :start-elements [#t("foo" 1 33)
                                                     #t("bar" 34 66)
                                                     #t("baz" 67 100)]
                                    :elements {"foo" [#t("bar" 1 50)
                                                      #t("baz" 51 100)]
                                               "bar" [#t("foo" 1 50)
                                                      #t("baz" 51 100)]
                                               "baz" [#t("foo" 1 50)
                                                      #t("bar" 51 100)]})]
            [chain (factory)])

(fact "markov chain can have multiple transitions from single element"
      (with-background foo-bar-baz [chain]
        (assert-that (take 500 chain)
                     (has-items "foo" "bar" "baz"))))
