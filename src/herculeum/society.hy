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

(require hymn.dsl)

(import [pyherc.utils [clamp-value]]
        [hymn.types.either [Right ->either failsafe]]
        [hymn.operations [>=>]])

(defn new-society [name]
  "create new society"
  {:name name
   :raw-resources medium
   :projects []
   :buildings []})


(def depleted 0)
(def very-low 1)
(def low 2)
(def medium 3)
(def high 4)
(def very-high 5)
(def overflowing 6)

(defn society-name [society &optional name]
  "get/set name of a society"
  (when name
    (assoc society :name name))
  (:name society))

(defn raw-resources [society &optional amount]
  "get/set amount of raw resources for a society"
  (when (not (nil? amount))
    (assoc society :raw-resources amount))
  (:raw-resources society))

(defn projects [society]
  "list of projects"
  (:projects society))

(defn start-project [society project]
  "start a new project"
  (.append (:projects society) project))

(defn complete-project [society project]
  "complete a project"
  (.remove (:projects society) project)
  (add-building society (:building project)))

(defn new-project [name &optional [duration 1] [building nil]]
  "create new project"
  {:name name
   :duration duration
   :building building})

(defn project-name [project &optional name]
  "get/set name of a project"
  (when name
    (assoc project :name name))
  (:name project))

(defn project-duration [project &optional duration]
  "get/set duration of a project"
  (when (not (nil? duration))
    (assoc project :duration duration))
  (:duration project))

(defn buildings [society]
  "list of buildings"
  (:buildings society))

(defn new-building [name &optional [produces 0]]
  "create new building"
  {:name name
   :raw-production produces})

(defn add-building [society building]
  "add new building"
  (.append (:buildings society) building))

(defn building-name [building &optional name]
  "get/set building name"
  (when (not (nil? name))
    (assoc building :name name))
  (:name building))

(defn building-production [building &optional amount]
  "get/set raw resource production"
  (when (not (nil? amount))
    (assoc building :raw-production amount))
  (:raw-production building))

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
