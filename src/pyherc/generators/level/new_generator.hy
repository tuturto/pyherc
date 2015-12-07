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

(require hy.contrib.anaphoric)
(require pyherc.macros)

(import [pyherc.data [new-level Portal add-portal get-locations-by-tag
                      wall-tile level-name level-description
                      safe-passage]]
        [pyherc.generators.level.partitioners.old-grid [RandomConnector]])

(defmacro run-generators-for [level &rest generators]
  `(do ~@(map (fn [x] `(ap-each ~x (it ~level))) generators)))

(defn new-level-generator [model partitioners room-generators decorators
                           portal-adders item-adders creature-adders
                           trap-generator
                           rng name description]
  "create a new level generator function"
  (fn [portal]
    (let [[level (new-level model)]
          [partitioner (.choice rng partitioners)]
          [connector (RandomConnector rng)]
          [sections (.connect-sections connector (partitioner level))]]
      (level-name level name)
      (level-description level description)
      (ap-each sections ((.choice rng room-generators) it trap-generator))
      (when creature-adders ((.choice rng creature-adders) level))
      (when item-adders ((.choice rng item-adders) level))
      (run-generators-for level
                          portal-adders
                          decorators)
      (when portal
        (let [[rooms (list-comp x [x (get-locations-by-tag level "room")]
                                (safe-passage level x))]]
          (when rooms (add-portal level
                                  (.choice rng rooms)
                                  (Portal #t(portal.other-end-icon nil) nil)
                                  portal))))
      level)))
