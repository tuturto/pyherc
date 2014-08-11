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

(import [hamcrest.core.base_matcher [BaseMatcher]])

(defclass SectionOverLapMatcher [BaseMatcher]
  [[--init-- (fn [self]
               "default constructor"
               (-> (super) (.--init--)))]
   [-matches (fn [self item]
               "check if given item matches"
               false)]
   [describe-to (fn [self description]
                  "describe matcher"
                  (.append description "unfinished matcher"))]
   [describe-mismatch (fn [self item mismatch-description]
                        "describe why item does not match"
                        (.append mismatch-description "mismatch"))]])

(defn are-not-overlapping []
  (SectionOverLapMatcher))
