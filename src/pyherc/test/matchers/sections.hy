;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2014 Tuukka Turto
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

(require hy.contrib.anaphoric)
(require pyherc.macros)

(import [hamcrest.core.base_matcher [BaseMatcher]]
        [pyherc.generators.level.partitioners [section-corners]])

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
                 (and (!= section another-section)
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
