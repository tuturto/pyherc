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


(require [hy.extra.anaphoric [ap-each]])
(require [pyherc.macros [*]])

(import [pyherc.ai [ai-state]]
        [pyherc.data.geometry [find-direction distance-between]]
        [pyherc.data [perception-range get-characters]]
        [pyherc.rules.perception [spotted?]]
        pyherc)

(defn select-current-enemy [character strategy]
  "select current target for this character"
  (assoc (ai-state character) :current-enemy 
         (strategy character (detected-enemies character))))

(defn current-enemy [character]
  "current enemy of this character"
  (if (in :current-enemy (ai-state character))
    (:current-enemy (ai-state character))
    None))

(defn closest-enemy [character enemies]
  "select enemy that is closest to given character"
  (let [enemy None]
    (ap-each enemies 
             (cond [(none? enemy)
                    (setv enemy #t(it (distance-between character it)))]
                   [(< (distance-between character it) (first enemy))
                    (setv enemy #t(it (distance-between character it)))]))
    (when enemy (first enemy))))

(defn melee [character target]
  "perform a melee attack of somekind against target"
  (call attack character
        (find-direction (. character location) (. target location))))

(defn detected-enemies [character]
  "has AI detected an enemy"
  (list (filter (fn [target]
                  (and (not (= character target))
                       (enemy? character target)
                       (spotted? character target)))
                (get-characters (. character level)))))

(defn enemy? [character target] ;; TODO: implement, move into data?
  "are these two characters enemies?"
  (not (= (. character name) (. target name))))
