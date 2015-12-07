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

(defmacro effect-dsl []
  `(do
    (import [pyherc.data.effects.effect [Effect]])
    (require pyherc.macros)))

(defmacro effect [type name attributes &rest body]
  "create a class that defines a new effect"
  (defn select-branch [x]
    (let [[key (first x)]
          [value (second x)]]
      (cond
       [(= key :trigger) `(method do-trigger [dying-rules] ~attributes ~value)]
       [(= key :add-event) `(method get-add-event [] ~attributes ~value)]
       [(= key :remove-event) `(method get-removal-event [] ~attributes ~value)]
       [true (macro-error key "key failure")])))
  (defn pair-list [data]
    (list (zip (slice data 0 nil 2)
               (slice data 1 nil 2))))
  (let [[pairs (pair-list body)]
        [multiples-pair (first (filter (fn [x] (= (first x) :multiple-allowed))
                                       pairs))]
        [multiple-status (if multiples-pair
                           (second multiples-pair)
                           'false)]]
    `(defclass ~type [Effect]
       [(effect-initializer ~name ~attributes ~multiple-status)
        ~@(list-comp (select-branch pair)
                     [pair pairs]
                     (in (first pair) [:trigger :add-event :remove-event]))])))

(defmacro effect-initializer [effect-name attributes multiples]
  "create --init-- method for effect"
  `[--init-- (fn [self duration frequency tick icon title
                  description ~@attributes]
               (super-init :duration duration
                           :frequency frequency
                           :tick tick
                           :icon icon
                           :title title
                           :description description)
               (set-attributes ~@attributes)
               (setv self.effect-name ~effect-name)
               (setv self.multiple-allowed ~multiples)
               nil)])

(defmacro method [name params attributes body]
  "create method used in effect class"
  `[~name (fn [self ~@params]
            (let [~@(genexpr `[~x (. self ~x)] [x attributes])]
              ~body))])

(defmacro check-dying [target]
  `(.check-dying dying-rules ~target))
