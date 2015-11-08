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

(require hy.contrib.anaphoric
         pyherc.macros)

(defmacro/g! fact [name desc &rest body]
  `(defun ~name [var1 var2]
     (let [[~g!func (fn [context updated-variable]
                      ~desc
                      (do ~@body))]]
       (.append var1.constraints ~g!func)
       (.append var2.constraints ~g!func))))

(defclass Variable []
  [[--init-- (fn [self &rest values]
               "default initializer"
               (setv self.values (set values))
               (setv self.constraints [])
               (setv self.last-save-frame-pointer -1)
               nil)]
   [--repr-- (fn [self]
              (str self.values))]])

(defn value [variable]
  "Get unique value of given variable"
  (if (unique? variable)
    (first variable.values)
    (assert false)))

(defn unique? [variable]
  "does variable have exactly one value"
  (= (len variable.values) 1))

(defn value? [variable]
  "does the variable have a valid value"
  (len variable.values))

(defn narrow [context variable values]
  "narrow down variable"
  (let [[new-values (& variable.values values)]]
    (if (= new-values (set []))
      false
      (if (= new-values variable.values)
        true
        (do (save context variable)
            (setv variable.values new-values)
            (all (genexpr (constraint context variable)
                          [constraint variable.constraints])))))))

(defn save [context variable]
  "save variable state in undo stack"
  (.append (:variable-stack context) variable)
  (.append (:value-stack context) variable.values)
  (setv variable.last-save-frame-pointer (:frame-pointer context)))

(defn restore-values [context variable frame-pointer]
  "restore variable states from undo stack"
  (while (> (len (:variable-stack context)) frame-pointer)
    (let [[var (.pop (:variable-stack context))]
          [vals (.pop (:value-stack context))]]
      (setv var.values vals)))
  (assoc context :frame-pointer frame-pointer))

(fact are-equal!
      "equality constraint"
      (if (= updated-variable var1)
        (narrow context var2 updated-variable.values)
        (narrow context var1 updated-variable.values)))

(fact are-inequal!
      "inequality constraint"
      (when (value? var1)
        (narrow context var2 (- var2.values var1.values)))
      (when (value? var2)
        (narrow context var1 (- var1.values var2.values))))

(fact less-than!
      "smaller than constraint"
      (let [[maximum (max updated-variable.values)]]
        (if (= updated-variable var1) 
          (narrow context var2 (set-comp x [x var2.values] (> x (min var1.values))))
          (narrow context var1 (set-comp x [x var1.values] (< x (max var2.values)))))))

(defun greater-than! [var1 var2]
  "greater than constraint"
  (less-than! var2 var1))

(defun in-between! [var1 var2 var3]
  "constraint something in-between two other things"
  (less-than! var2 var1)
  (less-than! var1 var3))

(defn solve [&rest variables]
  "solve all variables"
  (let [[context {:frame-pointer nil
                  :variable-stack []
                  :value-stack []
                  :solved false}]]
    (solve-one context variables)))

(defn solve-one [context variables]
  "solve all variables"  
  (if (all (map unique? variables))
    (do (assoc context :solved true)        
        variables)
    (let [[variable (variable-to-solve variables)]
          [frame (len (:variable-stack context))]]
      (assoc context :frame-pointer frame)
      (for [value variable.values]        
        (do (when (not (:solved context))
              (if (narrow context variable (set [value]))
                (do (if (all (map value? variables))
                      (if (not (solve-one context variables))
                        (assert false))))
                false))
            (when (not (:solved context))
              (restore-values context variable frame))))
      (when (:solved context)
        variables))))

(defn variable-to-solve [variables]
  "select next variable to solve"
  (first (filter (fn [x] (not (unique? x)))
                 variables)))
