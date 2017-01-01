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

(import [herculeum.society [building-name raw-resources]])

;; TODO: move this into Archimedes after Hy release
(defmacro defmatcher [matcher-name params &rest funcs]
  "define matcher class and function"
  (import [pyherc.utils [group]])
  
  (defn helper [match? match! no-match!]
    `(defn ~matcher-name ~params
       (import [hamcrest.core.base-matcher [BaseMatcher]])

       (defclass MatcherClass [BaseMatcher]
         [[--init-- (fn [self ~@params]
                      (set-attributes ~@params)
                      nil)]
          [-matches (fn [self item]
                      ~match?)]
          [describe-to (fn [self description]
                         (.append description ~match!))]
          [describe-mismatch (fn [self item mismatch-description]
                               (.append mismatch-description ~no-match!))]])
       
       (MatcherClass ~@params)))

  (apply helper [] (dict-comp (cond [(= (first x) :match?) "is_match"]
                                    [(= (first x) :match!) "match!"]
                                    [(= (first x) :no-match!) "no_match!"])
                              (second x)
                              [x (group funcs)])))

;; TODO: move this into Archimedes after Hy release
(defmacro attribute-matcher [matcher-name func pred match no-match]
  `(defmatcher ~matcher-name [value]
     :match? (~pred (~func item) value)
     :match! (.format ~match (. self value))
     :no-match! (.format ~no-match (~func item))))

(defmatcher has-building? [name]
  :match? (if item
            (any (filter (fn [x]
                           (= (building-name x)
                              (. self name)))
                         item))
            False)
  :match! (.format "a list with building '{0}'"
                   (. self name))
  :no-match! (if item
               (.format "was list of buildings: {0}"
                        (.join "," (map building-name item)))
               "was an empty list"))

(attribute-matcher has-resources?
                   raw-resources =
                   "a society with {0} resources"
                   "was a society with {0} resources")

(attribute-matcher has-more-resources-than?
                   raw-resources >
                   "a society with more than {0} resources"
                   "was a society with {0} resources")

(attribute-matcher has-less-resources-than?
                   raw-resources <
                   "a society with less than {0} resources"
                   "was a society with {0} resources")
