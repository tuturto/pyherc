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

(require [pyherc.macros [*]])
(import [pyherc.generators.artefact [create-blueprint modify-blueprint
                                     add-blueprint-type blueprint-types]]
        [herculeum.names [generate-random-name]]
        [random [Random]])

(defmacro/g! with-seed [seed-form mode &rest body]
  "build blueprint using given seed"
  (if (= (len seed-form) 1) (setv rng (first seed-form))
      (= (len seed-form) 2) (setv (, rng seed) seed-form)
      (> (len seed-form) 2) (macro-error seed-form 
                                         "did not understand parameters"))

  (if (< (len body) 2) (macro-error body
                                    "did not understand body (too short?)")
      (= (len body) 2) (setv (, sub-type code) body)
      (= (len body) 3) (setv (, bp-symbol sub-type code) body)
      (> (len body) 3) (macro-error body
                                    "did not understand body (too long?)"))

  (setv set-rng (if (= (len seed-form) 1)
                  `(if (in :seed ~bp-symbol)
                     (setv ~rng (Random (:seed ~bp-symbol)))
                     (setv ~rng (Random)))
                  `(setv ~rng (if ~seed
                                (Random ~seed)
                                (Random)))))

  (if (= mode :create) `(do ~set-rng
                            (setv ~g!temp ~code)
                            (assoc ~g!temp :seed ~seed)
                            (assoc ~g!temp :type ~sub-type)
                            (add-blueprint-type ~g!temp ~sub-type)
                            ~g!temp)
      (= mode :modify) `(do (if (not (in ~sub-type (blueprint-types ~bp-symbol)))
                              (do ~set-rng
                                  (add-blueprint-type ~bp-symbol ~sub-type)
                                  (merge-blueprints ~bp-symbol ~code))
                              (assert false (.format "{0} applied twice"
                                                     ~sub-type)))
                              ~bp-symbol)
      (macro-error mode (.format "mode {0} not in {1}"
                                 mode
                                 ['create 'modify]))))

(defn merge-blueprints [orig modification]
  "merge original and modifier blueprints together"
  (for [(, key value) (.items modification)]
    (if (in key orig)
      (if (is (type value) int) (assoc orig key (+ (get orig key) value))
          (is (type value) list) (.extend (get orig key) value)
          (assert "unknown type"))
      (assoc orig key value))))

(defmethod create-blueprint 'human [object-type &optional [seed None]]
  "create blueprint for human"
  (with-seed [rng seed] :create 'human
    {:name (generate-random-name (new-seed rng))
     :body (.randint rng 5 7)
     :finesse (.randint rng 5 7)
     :mind (.randint rng 5 7)
     :inventory []}))


(defmethod modify-blueprint 'wise [modifier-type blueprint]
  "modify blueprint to create wise character"
  (with-seed [rng] :modify blueprint 'wise
    {:mind (.randint rng 1 3)}))

(defmethod modify-blueprint 'smith [modifier-type blueprint]
  "modify blueprint to create smith"
  (with-seed [rng] :modify blueprint 'smith
    {:body (.randint rng 1 2)
     :mind (.randint rng -1 0)}))

(defmethod modify-blueprint 'scribe [modifier-type blueprint]
  "modify blueprint to create scribe"
  (with-seed [rng] :modify blueprint 'scribe
    {:body (.randint rng -1 0)
     :mind (.randint rng 1 2)
     :inventory [(create-blueprint 'scroll (new-seed rng))]}))

(defmulti instantiate-blueprints [&rest blueprints]
  "select method based on type in blueprint"
  (if (= (len blueprints) 1)
    (:type (first blueprints))
    (tuple (list-comp (:type blueprint) [blueprint blueprints]))))

(default-method instantiate-blueprints [&rest blueprints]
  "no definition found, thrown an error"
  (assert False "no instantiator found for blueprint"))

(defmethod instantiate-blueprints 'human [blueprint]
  "instantiate blueprint for human"
  None)

;; TODO: move somewhere common
(defn new-seed [rng]
  "create new random seed"
  (.randint rng 0 9223372036854775807))
