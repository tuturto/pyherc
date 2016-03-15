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
(require hy.contrib.anaphoric)
(import [pyherc.data.level [blocks-movement]]
        [pyherc.data.geometry [area-around area-4-around]]
        [functools [reduce]]
        [toolz [curry]])

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

(with-decorator curry
  (defn doorframe? [level location]
    "check if given location is door frame"
    (and (corridor? level location)
         (any (map (fn [x]
                     (and (not (blocks-movement level x))
                          (not (corridor? level x))))
                   (area-4-around location))))))

(defn open-area? [level location]
  "check if given location is in open area"
  (let [[#t(x y) location]
        [north #t(x (- y 1))]
        [south #t(x (+ y 1))]
        [east #t((+ x 1) y)]
        [west #t((- x 1) y)]]
    (and (not (blocks-movement level location))
         (not (blocks-movement level north))
         (not (blocks-movement level south))
         (not (blocks-movement level east))
         (not (blocks-movement level west)))))
