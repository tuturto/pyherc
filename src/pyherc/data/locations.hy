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

(require pyherc.macros)
(require hy.contrib.anaphoric)
(import [pyherc.data.level [blocks-movement]]
        [pyherc.data.geometry [area-around]]
        [functools [reduce]])

(defn corridor? [level location]
  "check if given location is surrounded from two sides"
  (let [[#t(x y) location]
        [north #t(x (- y 1))]
        [south #t(x (+ y 1))]
        [east #t((+ x 1) y)]
        [west #t((- x 1) y)]]
    (and (not (blocks-movement level location))
         (or (and (blocks-movement level north)
                  (blocks-movement level south)
                  (not (blocks-movement level east))
                  (not (blocks-movement level west)))
             (and (blocks-movement level east)
                  (blocks-movement level west)
                  (not (blocks-movement level north))
                  (not (blocks-movement level south)))))))

(defn next-to-wall? [level location]
  "check if given location is next to wall"
  (let [[#t(x y) location]
        [north #t(x (- y 1))]
        [south #t(x (+ y 1))]
        [east #t((+ x 1) y)]
        [west #t((- x 1) y)]]
    (and (not (blocks-movement level location))
         (or (blocks-movement level north)
             (blocks-movement level south)
             (blocks-movement level east)
             (blocks-movement level west))
         (not (and (blocks-movement level north)
                   (blocks-movement level south)))
         (not (and (blocks-movement level east)
                   (blocks-movement level west))))))

(defn open-area? [level location]
  "check if given location is in open area"
  (and (not (blocks-movement level location))
       (reduce (fn [a b] (and (not a) (not b)))
               (ap-map (blocks-movement level it) (area-around location)))))
