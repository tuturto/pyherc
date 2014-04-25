;; -*- coding: utf-8 -*-
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

(import logging)
(import [decorator [decorator]])

(defreader d [expr] `(with-decorator log-debug ~expr))

(defreader i [expr] `(with-decorator log-info ~expr))

(defn create-logger [log-level]
  "create a logger with specific log level"
  (with-decorator decorator
    (fn [wrapped-function &rest args &kwargs kwargs]
      (let [[logger-name wrapped-function.--name--]
        [logger (.getLogger logging logger-name)]
        [call-message (.join " " ["call" ":" (str args) (str kwargs)])]]
    (.log logger log-level call-message)
    (try (do
          (let [[result (apply wrapped-function args kwargs)]
            [result-message (.join " " ["return" ":" (str result)])]]
        (.log logger log-level result-message)
        result))
         (catch [Exception] (do
                 (.exception logger (.format "{0} has thrown an exception" logger-name))
                 (raise))))))))

(setv log-debug (create-logger logging.DEBUG))
(setv log-info (create-logger logging.INFO))
(setv log-warning (create-logger logging.WARNING))
(setv log-error (create-logger logging.ERROR))
(setv log-critical (create-logger logging.CRITICAL))

(defn no-logger [wrapped-function]
  "logger that does nothing"
  wrapped-function)

(defn set-logger [log-level silent]
  "set application wide logging level"
  (global log-debug)
  (global log-info)
  (global log-warning)
  (global log-error)
  (global log-critical)
  (cond [(= log-level "info") (setv log-debug no-logger)]
    [(= log-level "warning") (do
                  (setv log-debug no-logger)
                  (setv log-info no-logger))]
    [(= log-level "error") (do
                (setv log-debug no-logger)
                (setv log-info no-logger)
                (setv log-warning no-logger))]
    [(= log-level "critical") (do
                   (setv log-debug no-logger)
                   (setv log-info no-logger)
                   (setv log-warning no-logger)
                   (setv log-error no-logger))])
  (when silent
    (do (setv log-debug no-logger)
    (setv log-info no-logger)
    (setv log-warning no-logger)
    (setv log-error no-logger)
    (setv log-critical no-logger))))
