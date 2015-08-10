;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2015 Tuukka Turto
;;
;;   This file is part of pyherc.
;;
;;   pyherc is free software: you can redistribute it and/or modify
;;   it under the terms of the GNU General Public License as published by
;;   the Free Software Foundation, either version 3 of the License, or
;;   (at your option) any later version.
;;
;;   pyherc is distributed in the hope that it will be useful,
;;   but WITHOUT ANY WARRANTY; without even the implied warranty of
;;   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;   GNU General Public License for more details.
;;
;;   You should have received a copy of the GNU General Public License
;;   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

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
