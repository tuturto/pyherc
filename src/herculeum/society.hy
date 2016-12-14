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

(import [hymn.types.either [Right ->either failsafe]]
        [hymn.operations [>=>]])

(defn new-society [name]
  "create new society"
  {:name name
   :raw-resources 'medium
   :projects []
   :buildings []})

(def resource-levels ['depleted 'very-low 'low 'medium 
                      'high 'very-high 'overflowing])

(defn society-name [society &optional name]
  "get/set name of a society"
  (when name
    (assoc society :name name))
  (:name society))

(defn raw-resources [society &optional amount]
  "get/set amount of raw resources for a society"
  (when amount
    (if-not (in amount resource-levels)
            (raise (ValueError (.format "incorrect value: {0}"
                                        amount))))
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
  (.append (:buildings society) (:building project)))

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

(defn new-building [name]
  "create new building"
  {:name name})

(defn building-name [building &optional name]
  "get/set building name"
  (when (not (nil? name))
    (assoc building :name name))
  (:name building))

(def process-raw-resources-m
  (failsafe (fn  [society]
              "process raw resources of society"
              (Right society))))

(def process-projects-m
  (failsafe (fn [society]
              "process ongoing projects"              
              (setv completed 
                    (filter (fn [prj]
                              (project-duration prj 
                                                (dec (project-duration prj)))
                              (<= (project-duration prj) 0))
                            (projects society)))
              (ap-each completed (complete-project society it))
              society)))

(def advance-time-m (>=> process-raw-resources-m
                         process-projects-m))
