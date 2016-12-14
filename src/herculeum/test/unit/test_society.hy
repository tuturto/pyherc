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

(require archimedes)
(require hymn.dsl)

(import [hamcrest [assert-that is- equal-to has-item is-not :as is-not-]]
        [hymn.types.either [->either either]]
        [herculeum.society [new-society raw-resources society-name
                            new-project project-name projects start-project
                            buildings new-building building-name
                            project-duration process-projects-m]]
        [herculeum.test.matchers.society [has-building?]])

;; TODO: this should go into archimedes
(defmacro/g! assert-error [error-str code]
  "assert that an error is raised"
  `(let [[~g!result (try 
                     (do ~code
                         "no exception raised")
                     (catch [~g!e Exception]
                       (if (= (str ~g!e) ~error-str)
                         nil
                         (.format "expected: '{0}'\n  got: '{1}'"
                                  ~error-str
                                  (str ~g!e)))))]]     
     (when ~g!result
        (assert false ~g!result))))

;; TODO: move to archimedes?
(defmacro/g! assert-right [monad check]
  "helper macro for asserting Either.Right"
  `(either (fn [~g!fail] 
             (assert False (str ~g!fail)))
           (fn [~g!ok]
             ~check)
           ~monad))


(background high-society
            [society (new-society "high society")]
            [project (new-project "housing construction"
                                  :building (new-building "housing"))]
            [long-project (new-project "monolith" :duration 10)])

(fact "society can have a name"
      (with-background high-society [society]
        (assert-that (society-name society)
                     (is- (equal-to "high society")))
        (society-name society "low society")
        (assert-that (society-name society)
                     (is- (equal-to "low society")))))

(fact "raw resources of society can be manipulated"
      (with-background high-society [society]
        (raw-resources society 'low)
        (assert-that (raw-resources society)
                     (is- (equal-to 'low)))))

(fact "setting raw value to incorrect value raises an error"
      (with-background high-society [society]
        (assert-error "incorrect value: ridiculous"
                      (raw-resources society 'ridiculous))))

(fact "project can have a name"
      (with-background high-society [project]
        (assert-that (project-name project)
                     (is- (equal-to "housing construction")))
        (project-name project "pool construction")
        (assert-that (project-name project)
                     (is- (equal-to "pool construction")))))

(fact "project can be started"
      (with-background high-society [society project]
        (start-project society project)
        (assert-that (projects society) 
                     (has-item project))))

(fact "project has duration"
      (with-background high-society [project]
        (assert-that (project-duration project)
                     (is- (equal-to 1)))
        (project-duration project 5)
        (assert-that (project-duration project)
                     (is- (equal-to 5)))))

(fact "processing projects decreases their duration"
      (with-background high-society [society long-project]
        (start-project society long-project)
        (assert-right (do-monad [status (process-projects-m society)]
                                status)
                      (assert-that (project-duration long-project)
                                   (is- (equal-to 9))))))

(fact "completed projects are removed for queue"
      (with-background high-society [society project]
        (start-project society project)
        (assert-right (do-monad [status (process-projects-m society)]
                                status)
                      (assert-that (projects society)
                                   (is-not- (has-item project))))))

(fact "completed project adds a new building"
      (with-background high-society [society project]
        (start-project society project)
        (assert-right (do-monad [status (process-projects-m society)]
                                status)
                      (assert-that (buildings society)
                                   (has-building? "housing")))))

(fact "building has a name"
      (let [[building (new-building "small house")]]
        (assert-that (building-name building)
                     (is- (equal-to "small house")))
        (building-name building "large house")
        (assert-that (building-name building)
                     (is- (equal-to "large house")))))
