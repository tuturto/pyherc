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

(import [hy [HySymbol]])

(require hy.contrib.anaphoric)

(defmacro background [context-name &rest code]
  (let [[symbols (ap-map (first it) code)]
        [fn-name (HySymbol (.join "" ["setup_" context-name]))]]
    `(defn ~fn-name []
       ~(.join "" ["setup context " context-name])
       (let [~@code]
         ~(dict-comp (keyword x) x [x symbols])))))

(defmacro fact [desc &rest code]
  (let [[fn-name (HySymbol (.join "" ["test " desc]))]]
    `(defn ~fn-name []
       ~desc
       ~@code)))

(defmacro/g! with-background [context-name symbols &rest code]    
  (let [[fn-name (HySymbol (.join "" ["setup_" context-name]))]]
    `(let [[~g!context (~fn-name)]
           ~@(ap-map `[~it (get ~g!context ~(keyword it))] symbols)]
       ~@code)))
