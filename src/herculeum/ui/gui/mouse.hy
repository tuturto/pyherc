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

(require [pyherc.macros [call]])

(import pyherc
        [pyherc.data [get-character]]
        [pyherc.data.geometry [find-direction]]
        [pyherc.ai.pathfinding [a-star :as a*]]
        [herculeum.ai.movement [whole-level]]
        [PyQt4.QtCore [Qt]])

(def find-path (a* (whole-level)))

(defn move? [event player click-location]
  "does player want to move?"
  (and (= (.button event) Qt.LeftButton)
       (not (get-character player.level click-location))))

(defn move [event player click-location]
  "move within level"
  (let [location player.location
        level player.level
        (, path connections, updated) (find-path location
                                                 click-location
                                                 level)]
    (when (and path (> (len path) 1))
      (call move player (find-direction location (second path))))))
