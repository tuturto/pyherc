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

(require pyherc.macros)

(import [random [Random]]
        [pyherc.data [Item]]
        [pyherc.data.effects [EffectsCollection]]
        [pyherc.generators.artefact [generate-artefact create-blueprint
                                     instantiate-blueprints]]
        [herculeum.names [generate-random-name]])

(def *name-forms*
  {'litany    "litanies"
   'scripture "scriptures"
   'prayer    "prayer"})

(def *tube-materials*
  {'wood   #t("wooden" 0.8)
   'iron   #t("iron"   0.9)
   'brass  #t("brass"  1.0)
   'silver #t("silver" 1.1)
   'onyx   #t("onyx"   1.2)
   'ivory  #t("ivory"  1.3)
   'gold   #t("golden" 1.4)})

(def *tube-qualities*
  {'plan          #t("plain"              0.9)
   'ornate        #t("ornate"             1.0)
   'decorated     #t("decorated"          1.1)
   'carved        #t("beautifully carved" 1.2)
   'very-ornate   #t("very ornate"        1.3)
   'mastercrafted #t("mastercrafted"      1.4)})

(def *paper-materials*
  {'parchment #t("parchment" 1.0)
   'papyrus   #t("papyrus"   1.1)
   'paper     #t("paper"     1.2)
   'vellum    #t("vellum"    1.3)})

(def *paper-conditions*
  {'teared-lot     #t("has torn in many places" 0.7)
   'holes          #t("has several holes"       0.8)
   'teared         #t("has torn a bit"          0.9)
   'faded          #t("has faded"               1.0)
   'well-preserved #t("is well preserved"       1.1)
   'like-new       #t("is like new"             1.2)})

(def *writing-qualities*
  {'shoddy      #t("shoddy quality"    0.9)
   'good        #t("good quality"      1.0)
   'very-good   #t("very good quality" 1.1)
   'mastercraft #t("mastercrafted"     1.2)})

(def *writing-details*
  {'plan        #t("plain"       1.0)
   'ornate      #t("ornate"      1.1)
   'decorated   #t("decorative"  1.2)
   'very-ornate #t("very ornate" 1.3)})

(def *virtues*
  ["Honesty" "Compassion" "Valor" "Justice" "Sacrifice"
             "Honor" "Spirituality" "Humility"])

(defn scroll-price [blueprint]
  "calculate price of scroll based on blueprint"
  (int (* 500
          (second (get *tube-materials* (:material (:tube blueprint))))
          (second (get *tube-qualities* (:quality (:tube blueprint))))
          (second (get *paper-materials* (:material (:paper blueprint))))
          (second (get *paper-conditions* (:condition (:paper blueprint))))
          (second (get *writing-qualities* (:quality (:writing blueprint))))
          (second (get *writing-details* (:detail (:writing blueprint)))))))

(defmethod create-blueprint 'scroll [artefact-type &optional [seed nil]]
  "create blueprint for a scroll"  
  (setv rng (if seed
              (Random seed)
              (Random)))
  {:type 'scroll
   :name (create-blueprint 'scroll-name :seed (new-seed rng))
   :tube (create-blueprint 'scroll-tube :seed (new-seed rng))
   :paper (create-blueprint 'scroll-paper :seed (new-seed rng))
   :writing (create-blueprint 'scroll-writing :seed (new-seed rng))})

(defmethod create-blueprint 'scroll-name [artefact-type &optional [seed nil]]
  "create blueprint for scroll name"
  (setv rng (if seed
              (Random seed)
              (Random)))
  (if (= 1 (.randint rng 1 2))
    (do (setv owner-name (generate-random-name (new-seed rng)))
        (setv owner-type 'person))
    (do (setv owner-name (.choice rng *virtues*))
        (setv owner-type 'virtue)))  
  {:type 'scroll-name
   :form (random-key *name-forms* rng)
   :owner owner-name
   :owner-type owner-type})

(defmethod create-blueprint 'scroll-tube [artefact-type &optional [seed nil]]
  "create blueprint for scroll tube"
  (setv rng (if seed
              (Random seed)
              (Random)))  
  {:type 'scroll-tube
   :quality (random-key *tube-qualities* rng)
   :material (random-key *tube-materials* rng)})

(defmethod create-blueprint 'scroll-paper [artefact-type &optional [seed nil]]
  "create blueprint for scroll paper"
  (setv rng (if seed
              (Random seed)
              (Random)))
  {:type 'scroll-paper
   :material (random-key *paper-materials* rng)
   :condition (random-key *paper-conditions* rng)
   :detail 'seal})

(defmethod create-blueprint 'scroll-writing [artefact-type &optional [seed nil]]
  (setv rng (if seed
              (Random seed)
              (Random)))
  {:type 'scroll-writing
   :quality (random-key *writing-qualities* rng)
   :detail (random-key *writing-details* rng)})

(defmethod instantiate-blueprints 'scroll [blueprint]
  "create a scroll based on blueprint"
  (let [[scroll-name (instantiate-blueprints (:name blueprint))]
        [name-parts (.split scroll-name :maxsplit 1)]
        [upper-case-name (.join " " [(.capitalize (first name-parts))
                                     (second name-parts)])]
        [tube (instantiate-blueprints (:tube blueprint))]
        [paper (instantiate-blueprints (:paper blueprint) (:writing blueprint))]
        [scroll-description (.join ""
                                   [(.capitalize tube) " containing "
                                    scroll-name ". "
                                    (.capitalize paper) "."])]]

    (setv new-item (Item (EffectsCollection)))
    (setv (. new-item name) upper-case-name)
    (setv (. new-item description) scroll-description)
    (setv (. new-item icon) "tied-scroll")
    (setv (. new-item weight) 1)
    (setv (. new-item cost) (scroll-price blueprint))
    (setv (. new-item tags) ["scroll" "hint" "artifact"])
    new-item))

(defmethod instantiate-blueprints 'scroll-name [blueprint]
  (.join " " [(get *name-forms* (:form blueprint))
              "of"
              (:owner blueprint)]))

(defmethod instantiate-blueprints 'scroll-tube [blueprint]
  (.join " " [(first (get *tube-qualities* (:quality blueprint)))
              (first (get *tube-materials* (:material blueprint)))
              "tube"]))

(defmethod instantiate-blueprints #t('scroll-paper 'scroll-writing) [paper-blueprint writing-blueprint]
  "get description for paper and the writing on it"
  (.join " " [(first (get *paper-materials* (:material paper-blueprint)))
              (first (get *paper-conditions* (:condition paper-blueprint)))
              (get-conjuction-for-paper-and-writing paper-blueprint writing-blueprint)
              (first (get *writing-qualities* (:quality writing-blueprint)))
              "writing is"
              (first (get *writing-details* (:detail writing-blueprint)))]))

(defn positive-writing? [quality]
  "is writing quality positive?"
  (in quality ['good 'very-good 'mastercraft]))

(defn positive-paper? [condition]
  "is paper in positive condition?"
  (in condition ['well-preserved 'like-new]))

(defn get-conjuction-for-paper-and-writing [paper-blueprint writing-blueprint]
  "get conjuction used in describing paper and writing"
  (let [[writing (:quality writing-blueprint)]
        [paper (:condition paper-blueprint)]]
    (cond [(and (positive-writing? writing)
                (positive-paper? paper)) "and"]
          [(and (not (positive-writing? writing))
                (not (positive-paper? paper))) "and"]
          [true "but"])))

(defn random-key [coll rng]
  "pick random key from dictionary"
  (setv res (list (.keys coll)))
  (.sort res)
  (.choice rng res))

(defn new-seed [rng]
  "create new random seed"
  (.randint rng 0 9223372036854775807))
