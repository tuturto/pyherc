;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2017 Tuukka Turto
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

(require [hymn.dsl [*]])
(require [pyherc.macros [*]])

(import [herculeum.society.data [raw-resources building-production buildings
                                 raw-resources projects complete-project
                                 project-duration depleted overflowing]]
        [pyherc.utils [clamp-value]]
        [hymn.types.either [Right ->either failsafe]]
        [hymn.operations [>=>]])

(def process-raw-resources-m
  (failsafe (fn  [society]
              "process raw resources of society"
              (raw-resources society
                             (reduce (fn [accum bld]
                                       (+ accum (building-production bld)))
                                     (buildings society)
                                     (raw-resources society)))
              society)))

(def process-projects-m
  (failsafe (fn [society]
              "process ongoing projects"              
              (setv completed 
                    (filter (fn [prj]
                              (project-duration prj 
                                                (dec (project-duration prj)))
                              (raw-resources society 
                                             (dec (raw-resources society)))
                              (<= (project-duration prj) 0))
                            (projects society)))
              (ap-each completed (complete-project society it))
              society)))

(def clamp-values-m
  (failsafe (fn [society]
              "clamp values to their range"
              (clamp-value society raw-resources depleted overflowing))))

(def advance-time-m (>=> process-raw-resources-m
                         process-projects-m
                         clamp-values-m))
