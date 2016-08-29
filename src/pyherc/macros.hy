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

(require hy.contrib.anaphoric)

(defreader t [expr] `(, ~@expr))

(defmacro x-coordinate [location] `(first ~location))
(defmacro y-coordinate [location] `(second ~location))

(defmacro count [seq]
  (with-gensyms [counter]
    `(let [[~counter 0]]
      (ap-each ~seq (setv ~counter (+ 1 ~counter)))
      ~counter)))

(defmacro ylet [&rest args] `(yield-from (let ~@args)))

;; TODO: remove this if it ever lands Hy
(defmacro xor [&rest args]
  "perform exclusive or comparison between all arguments"
  (when (< (len args) 2) (macro-error nil "xor requires at least two arguments."))
  `(= (reduce (fn [a b] (if b (inc a) a)) ~args 0) 1))

(defmacro super-init [&rest args &kwargs kwargs]
  "call super --init-- with given parameters"
  (cond [(and args kwargs) `(-> (super)
                                (.--init-- ~@args ~kwargs))]
        [args `(-> (super)
                   (.--init-- ~@args))]
        [kwargs `(-> (super)
                     (.--init-- ~kwargs))]
        [true `(-> (super)
                   (.--init--))]))

(defmacro set-attributes [&rest attributes]
  "set attributes of object with respective parameters in --init--"
  `(do ~@(genexpr `(setv (. self ~x) ~x) [x attributes])))

(defmacro when-not [check &rest body]
  "like when, but inversed"
  `(when (not ~check) ~@body))

(defmacro none [coll]
  "like any, but inversed"
  `(not (any ~coll)))

(defreader s [data]
  "simple string joiner"
  `(.join " " [~@data]))

(defmacro defn+ [fn-name parameters &rest code]
  "create function and place it in vtable"
  `(do (import [pyherc])
       (assoc (. pyherc vtable) ~(keyword fn-name) (fn ~parameters ~@code))))

(defmacro call [fn-name &rest parameters]
  "call function in vtable"
  `((get (. pyherc vtable) ~(keyword fn-name)) ~@parameters))

(defmacro one-of [&rest actions]
  "perform one of following actions randomly"
  `((.choice random [~@(ap-map `(fn [] ~it) actions)])))

(defn multi-decorator [dispatch-fn]
  (setv inner (fn [&rest args &kwargs kwargs]
                (setv dispatch-key (apply dispatch-fn args kwargs))
                (if (in dispatch-key inner.--multi--)
                  (apply (get inner.--multi-- dispatch-key) args kwargs)
                  (apply inner.--multi-default-- args kwargs))))
  (setv inner.--multi-- {})
  (setv inner.--doc-- dispatch-fn.--doc--)
  (setv inner.--multi-default-- (fn [&rest args &kwargs kwargs] nil))
  inner)
 
(defn method-decorator [dispatch-fn &optional [dispatch-key nil]]
  (fn [func]
    (if (is dispatch-key nil)
      (setv dispatch-fn.--multi-default-- func)
      (assoc dispatch-fn.--multi-- dispatch-key func))
    dispatch-fn))

(defmacro defmulti [name params &rest body]
  `(do (import [pyherc.macros [multi-decorator]])
       (with-decorator multi-decorator
         (defn ~name ~params ~@body))))
 
(defmacro defmethod [name multi-key params &rest body]
  `(do (import [pyherc.macros [method-decorator]])
       (with-decorator (method-decorator ~name ~multi-key)
         (defn ~name ~params ~@body))))
 
(defmacro default-method [name params &rest body]
  `(do (import [pyherc.macros [method-decorator]])
       (with-decorator (method-decorator ~name)
         (defn ~name ~params ~@body))))

(defmacro/g! left-if-nil [params &rest code]
  #s("check params for nils and return (Left ret-value) if any is nil."
     "otherwise, execute code and return (Right ret-value).")
  `(do (setv ~g!pairs (zip ~(list (map name params)) ~params))
       (setv ~g!check (list (filter (fn [x] (not (nil? x)))
                                    (map (fn [x]
                                           (when (nil? (second x)) (first x)))
                                         ~g!pairs))))
       (if ~g!check
         (do (import inspect)
             (setv ~g!frame (first (.stack inspect)))             
             (Left (.format "following values were nil: {0} (function: {1} in file: {2})"
                            (.join "," ~g!check)
                            (get ~g!frame 3)
                            (get ~g!frame 1))))
         (do ~@code))))

(defmacro/g! do-monad-e [&rest code]
  "run monadic computation and print out (Left x) on console"
  `(do (setv ~g!result (do-monad ~@code))
       (when (left? ~g!result)
         (print ~g!result))
       ~g!result))
