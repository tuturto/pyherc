;; -*- coding: utf-8 -*-
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
 
(import logging)
(import [decorator [decorator]])

(defreader d [expr] `(with-decorator log-debug ~expr))

(defreader i [expr] `(with-decorator log-info ~expr))

(defn create-logger [log-level]
  "create a logger with specific log level"
  (with-decorator decorator
    (fn [wrapped-function &rest args &kwargs kwargs]
      (let [logger-name wrapped-function.--name--
            logger (.getLogger logging logger-name)
            call-message (.join " " ["call" ":" (str args) (str kwargs)])]
        (.log logger log-level call-message)
        (try (do
              (let [result (apply wrapped-function args kwargs)
                    result-message (.join " " ["return" ":" (str result)])]
                (.log logger log-level result-message)
                result))
             (except [Exception]
               (do
                (.exception logger (.format "{0} has thrown an exception"
                                            logger-name))
                (raise))))))))

(defn no-logger [wrapped-function]
  "logger that does nothing"
  wrapped-function)

(setv log-debug no-logger)
(setv log-info no-logger)
(setv log-warning no-logger)
(setv log-error no-logger)
(setv log-critical no-logger)

(defn set-logger [log-level]
  "set application wide logging level"
  (global log-debug)
  (global log-info)
  (global log-warning)
  (global log-error)
  (global log-critical)
  (cond [(= log-level "debug") 
         (do
          (setv log-debug (create-logger logging.DEBUG))
          (setv log-info (create-logger logging.INFO))
          (setv log-warning (create-logger logging.WARNING))
          (setv log-error (create-logger logging.ERROR))
          (setv log-critical (create-logger logging.CRITICAL)))]
         [(= log-level "info") 
          (do
           (setv log-info (create-logger logging.INFO))
           (setv log-warning (create-logger logging.WARNING))
           (setv log-error (create-logger logging.ERROR))
           (setv log-critical (create-logger logging.CRITICAL)))]
         [(= log-level "warning") 
          (do
           (setv log-warning (create-logger logging.WARNING))
           (setv log-error (create-logger logging.ERROR))
           (setv log-critical (create-logger logging.CRITICAL)))]
         [(= log-level "error") 
          (do
           (setv log-error (create-logger logging.ERROR))
           (setv log-critical (create-logger logging.CRITICAL)))]
         [(= log-level "critical") 
          (do
           (setv log-critical (create-logger logging.CRITICAL)))]))
