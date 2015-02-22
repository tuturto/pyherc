;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2015 Tuukka Turto
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

(require pyherc.macros)

(import [pyherc.generators.level.partitioners.section [new-section
                                                       mark-all-neighbours]])

(defn grid-partitioning [room-size horizontal-repeats vertical-repeats rng]
  "create a new partitioner"
  (fn [level]
    "partition a level"    
    (let [[sections []]
          [#t(width height) room-size]] 
      (for [x (range horizontal-repeats)]
        (for [y (range vertical-repeats)]
          (.append sections 
                   (new-section #t((* width x) (* height y)) 
                                #t((+ 1 (* width (+ x 1)))
                                   (+ 1 (* height (+ y 1)))) 
                                level 
                                rng))))
      (mark-all-neighbours sections)
      sections)))
