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
(require pyherc.macros)

(import [hamcrest.core.base_matcher [BaseMatcher]]
        [pyherc.generators.level.partitioners [section-corners
                                               equal-sections?]])

(defclass SectionOverLapMatcher [BaseMatcher]
  [[--init-- (fn [self]
               "default constructor"
               (-> (super) (.--init--)))]
   [-matches (fn [self item]
               "check if given item matches"
               (if (any (ap-map (overlapping? it item) item))
                 false
                 true))]
   [describe-to (fn [self description]
                  "describe matcher"
                  (.append description "list of not overlapping sections"))]
   [describe-mismatch (fn [self item mismatch-description]
                        "describe why item does not match"
                        (.append mismatch-description 
                                 (describe-sections item)))]])

(defn overlapping? [section sections]
  (any (ap-map (let [[another-section it]]
                 (and (not (equal-sections? section another-section))
                      (any (ap-map (inside-square? it
                                                   another-section)
                                   (all-corners section)))))
               sections)))

(defn inside-square? [point section]
  "is given point inside of a section?"
  (let [[#t(point₀ point₁) (section-corners section)]]
    (and
     (<= (x-coordinate point₀) (x-coordinate point) (x-coordinate point₁))
     (<= (y-coordinate point₀) (y-coordinate point) (y-coordinate point₁)))))

(defn all-corners [section]
  "get list containing all corners of a section"
  (let [[#t(corner₀ corner₁) (section-corners section)]]
    [corner₀ corner₁
     #t((x-coordinate corner₀) (y-coordinate corner₁))
     #t((x-coordinate corner₁) (y-coordinate corner₀))]))

(defn describe-sections [sections]
  (.format "sections with corners: {0}"
           (.join " " (ap-map (str (section-corners it)) sections)))) 

(defn are-not-overlapping []
  (SectionOverLapMatcher))
