;; -*- coding: utf-8 -*-
;;
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

(require hy.contrib.anaphoric)
(require pyherc.macros)

(import [functools [partial]]
        [itertools [chain]]
        [pyherc.generators.level.partitioners.section [new-section
                                                       left-edge right-edge
                                                       top-edge bottom-edge
                                                       section-corners
                                                       section-level
                                                       section-width
                                                       section-height]])

(defn binary-space-partitioning [level-size room-min-size rng]
  "create a new partitioner"
  (fn [level]
    "partition a level"
    (let [[section (new-section #t(0 0) level-size level rng)]]
      (partition-section level-size room-min-size rng section))))

(defn partition-section [level-size room-min-size rng section]
  "recursively partition a section"
  (let [[split-directions (possible-splits room-min-size section)]]
    (if (= (len split-directions) 0)
      [section]
      (let [[direction (.choice rng split-directions)]
            [new-sections (split-section section direction room-min-size rng)]]
        (.from-iterable chain (ap-map (partition-section level-size
                                                         room-min-size
                                                         rng
                                                         it)               
                                      new-sections))))))

(defn possible-splits [room-min-size section]
  "produce list of possible ways to split a section"
  (let [[directions []]]
    (if (< (* 2 (first room-min-size)) (section-width section))
      (.append directions :horizontal))
    (if (< (* 2 (second room-min-size)) (section-height section))
      (.append directions :vertical))
    directions))

(defn split-section [section direction room-min-size rng]
  "split section to a given direction"
  (cond [(= direction :horizontal) (split-horizontally section 
                                                       room-min-size 
                                                       rng)]
        [(= direction :vertical) (split-vertically section
                                                   room-min-size
                                                   rng)]))

(defn random-cut-point [start end size rng]
  "select a random point between start and end, while leaving enough
   space for size in the middle"
  (.randint rng (+ start size) (- end size)))

(defn split-horizontally [section room-min-size rng]
  (let [[level (section-level section)]
        [corners (section-corners section)]
        [cut-point (random-cut-point (left-edge section)
                                     (right-edge section)
                                     (first room-min-size)
                                     rng)]        
        [section₀ (new-section (first corners) 
                               #t(cut-point 
                                  (y-coordinate (second corners)))
                               level rng)]
        [section₁ (new-section #t((+ cut-point 1)
                                  (y-coordinate (first corners)))
                               (second corners)
                               level rng)]]
    [section₀ section₁]))

(defn split-vertically [section room-min-size rng]
  (let [[level (section-level section)]
        [corners (section-corners section)]
        [cut-point (random-cut-point (top-edge section)
                                     (bottom-edge section)
                                     (second room-min-size)
                                     rng)]        
        [section₀ (new-section (first corners) 
                               #t((x-coordinate (second corners))
                                  cut-point)
                               level rng)]
        [section₁ (new-section #t((x-coordinate (first corners))
                                  (+ cut-point 1))
                               (second corners)
                               level rng)]]
    [section₀ section₁]))
