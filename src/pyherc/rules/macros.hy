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

(defmacro date-rules [&rest rule-specs]
  `(defn get-special-events [year month day]
     (let [[events []]]
       ~@(map (fn [x] `(date-rule ~@x)) rule-specs)
       events)))

(defmacro date-rule [date-name &rest rules]
  (if (> (len rules) 1)
    `(when (and ~@rules) (.append events ~date-name))
    `(when ~@rules (.append events ~date-name))))

(defmacro action-interface-dsl []
  `(import [hymn.types.maybe [nothing?]]
           [pyherc.ports [interface]]
           pyherc))

(defmacro/g! run-action [param]
  `(let [[~g!action (interface.*factory* ~param)]]
     (if (nothing? ~g!action)
       (assert false "no suitable factory found")
       (.execute (.from-maybe ~g!action nil)))))

(defmacro/g! legal-action? [param]
  `(let [[~g!action (interface.*factory* ~param)]]
     (if (nothing? ~g!action)
       false
       (.legal? (.from-maybe ~g!action nil)))))

(defmacro defparams [name type attributes]
  `(defclass ~name []
     [[--init-- (fn [self ~@attributes]
                  (set-attributes ~@attributes)
                  (setv self.action-type ~type)
                  nil)]]))

(defmacro action-dsl []
  `(import [hy [HySymbol]]))

(defmacro defaction [name description &rest param-list]
  #s("define action class\n"
     "for now dying rules are implicitly passed in, but in the future this will be removed "
     "in favour of having global access to dying rules via vtable.")
  (setv action-name (HySymbol (.join "" [(.title name) "Action"])))

  (setv pair-list
    (list (zip (slice param-list 0 nil 2)
               (slice param-list 1 nil 2))))

  (setv init-params [])
  (setv legal-action nil)
  (setv illegal-action nil)
  (setv legal-check nil)
  (setv str-code `("no string representation has been defined for this action"))

  (ap-each pair-list (cond [(= (first it) :parameters)
                            (setv init-params (second it))]
                           [(= (first it) :legal-action)
                            (setv legal-action (second it))]
                           [(= (first it) :illegal-action)
                            (setv illegal-action (second it))]
                           [(= (first it) :legal?)
                            (setv legal-check (second it))]
                           [(= (first it) :to-string)
                            (setv str-code (second it))]
                           [true (macro-error nil (.join "" ["unknown parameter: " (first it)]))]))

  (when (is legal-action nil) (macro-error nil "legal action was not defined"))
  (when (is illegal-action nil) (macro-error nil "illegal action was not defined"))
  (when (is legal-check nil) (macro-error nil "legality check was not defined"))
  
  `(defclass ~action-name []
     ~description
     [[--init-- (fn [self ~@init-params]
                  "default initializer"
                  (super-init)
                  (set-attributes ~@init-params)
                  nil)]
      [execute #i(fn [self]
                   #s("execute this action\n"
                      "This should return Right X when everything was succesfully completed. "
                      "Otherwise this will return Left X.")
                   (if (.legal? self)
                     ~legal-action
                     ~illegal-action))]
      [legal? #d(fn [self]
                  "check if the action is legal enough to be executed"
                  ~legal-check)]
      [--str-- (fn [self]
                 "string representation of this action"
                 ~str-code)]]))
