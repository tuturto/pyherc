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
(require archimedes)

(import [herculeum.society.data [building-name raw-resources]]
        [pyherc.generators.artefact [blueprint-types]])

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

(defmatcher blueprint-for [blueprint-type]
  :match? (in (. self blueprint-type)
              (blueprint-types item))
  :match! (.format "a blueprint for '{0}'"
                   (. self blueprint-type))
  :no-match! (.format "was blueprint with: {0}"
                      (blueprint-types item)))

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
