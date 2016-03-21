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
    (assert false 
            (.format "variable is not unique: {0}" variable.values))))

(defn unique? [variable]
  "does variable have exactly one value"
  (= (len variable.values) 1))

(defn value? [variable]
  "does the variable have a valid value"
  (len variable.values))

(defn narrow [context variable values]
  "narrow down variable. true if ok, false if not ok"
  (let [[new-values (& variable.values values)]
        [res true]]
    (if (= new-values (set []))
      false
      (if (= new-values variable.values)
        true
        (do (save context variable)
            (setv variable.values new-values)
            (for [constraint (. variable constraints)]
              (setv res (constraint context variable))
              (when (not res)
                (break)))
            res)))))

(defn save [context variable]
  "save variable state in undo stack"
  (.append (:variable-stack context) variable)
  (.append (:value-stack context) variable.values)
  (setv variable.last-save-frame-pointer (frame-pointer context)))

(defn restore-values [context variable frame]
  "restore variable states from undo stack"
  (while (> (len (:variable-stack context)) frame)
    (let [[var (.pop (:variable-stack context))]
          [vals (.pop (:value-stack context))]]
      (setv var.values vals)))
  (frame-pointer context frame))

(fact are-equal!
      "equality constraint"      
      (if (= updated-variable var1)
        (narrow context var2 updated-variable.values)
        (narrow context var1 updated-variable.values)))

(fact are-inequal!
      "inequality constraint"      
      (cond [(and (= updated-variable var1)
                  (unique? var1))
             (narrow context var2 (- var2.values var1.values))]
            [(and (= updated-variable var2)
                  (unique? var2))
             (narrow context var1 (- var1.values var2.values))]
            [true true]))

(fact less-than!
      "smaller than constraint"
      (let [[maximum (max updated-variable.values)]]
        (if (= updated-variable var1) 
          (narrow context var2 (set-comp x [x var2.values] (> x (min var1.values))))
          (narrow context var1 (set-comp x [x var1.values] (< x (max var2.values)))))))

(defn greater-than! [var1 var2]
  "greater than constraint"
  (less-than! var2 var1))

(defn in-between! [var1 var2 var3]
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
  "solve all variables, one by one"
  (if (all (map unique? variables))
    (mark-solved context)
    (let [[variable (variable-to-solve variables)]
          [values (.copy variable.values)]
          [frame (len (:variable-stack context))]]
      (frame-pointer context frame)
      (for [value values]
        (if (not (solved? context))
          (if (narrow context variable (set [value]))
            (solve-one context variables)
            (do (restore-values context variable frame)
                (continue))) ;; narrowing failed and stack was restored, try next value
          (break))))) ;; solution was found, break loop  
  (if (solved? context) ;; we either have solution or no suitable value was found
    variables
    nil))

(defn frame-pointer [context &optional [frame nil]]
  "set or retrieve frame-pointer"
  (when (not (is frame nil))
    (assoc context :frame-pointer frame))
  (:frame-pointer context))

(defn mark-solved [context]
  "mark context as solved"
  (assoc context :solved true))

(defn solved? [context]
  "has the context been solved?"
  (:solved context))

(defn variable-to-solve [variables]
  "select next variable to solve"
  (first (filter (fn [x] (not (unique? x)))
                 variables)))
