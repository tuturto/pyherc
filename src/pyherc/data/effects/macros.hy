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
