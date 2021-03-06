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

(require [hy.extra.anaphoric [ap-map]])
(require [pyherc.macros [*]])

(import [functools [partial]]
        [itertools [chain]]
        [pyherc.generators.level.partitioners.section [new-section
                                                       left-edge right-edge
                                                       top-edge bottom-edge
                                                       section-corners
                                                       section-level
                                                       section-width
                                                       section-height
                                                       mark-all-neighbours]])

(defn binary-space-partitioning [level-size room-min-size rng]
  "create a new partitioner"
  (fn [level]
    "partition a level"
    (let [section (new-section #t(0 0) level-size level rng)
          sections (list (partition-section level-size 
                                            room-min-size 
                                            rng 
                                            section))]
      (mark-all-neighbours sections)
      sections)))

(defn partition-section [level-size room-min-size rng section]
  "recursively partition a section"
  (let [split-directions (possible-splits room-min-size section)]
    (if (= (len split-directions) 0)
      [section]
      (let [direction (.choice rng split-directions)
            new-sections (split-section section direction room-min-size rng)]
        (.from-iterable chain (ap-map (partition-section level-size
                                                         room-min-size
                                                         rng
                                                         it)               
                                      new-sections))))))

(defn possible-splits [room-min-size section]
  "produce list of possible ways to split a section"
  (let [directions []]
    (if (< (* 2 (first room-min-size)) (section-width section))
      (.append directions "horizontal"))
    (if (< (* 2 (second room-min-size)) (section-height section))
      (.append directions "vertical"))
    directions))

(defn split-section [section direction room-min-size rng]
  "split section to a given direction"
  (if (= direction "horizontal") (split-horizontally section 
                                                     room-min-size 
                                                     rng)
      (= direction "vertical") (split-vertically section
                                                 room-min-size
                                                 rng)))

(defn random-cut-point [start end size rng]
  "select a random point between start and end, while leaving enough
   space for size in the middle"
  (.randint rng (+ start size) (- end size)))

(defn split-horizontally [section room-min-size rng]
  (let [level (section-level section)
        corners (section-corners section)
        cut-point (random-cut-point (left-edge section)
                                    (right-edge section)
                                    (first room-min-size)
                                    rng)        
        section₀ (new-section (first corners) 
                              #t(cut-point 
                                 (y-coordinate (second corners)))
                              level rng)
        section₁ (new-section #t((+ cut-point 1)
                                 (y-coordinate (first corners)))
                              (second corners)
                              level rng)]
    [section₀ section₁]))

(defn split-vertically [section room-min-size rng]
  (let [level (section-level section)
        corners (section-corners section)
        cut-point (random-cut-point (top-edge section)
                                    (bottom-edge section)
                                    (second room-min-size)
                                    rng)        
        section₀ (new-section (first corners) 
                              #t((x-coordinate (second corners))
                                 cut-point)
                              level rng)
        section₁ (new-section #t((x-coordinate (first corners))
                                 (+ cut-point 1))
                              (second corners)
                              level rng)]
    [section₀ section₁]))
