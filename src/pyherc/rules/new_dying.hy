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

(import [pyherc.data.model [*died-in-dungeon* *escaped-dungeon*]]
        [pyherc.events [new-death-event new-drop-event]]
        [pyherc.data [remove-character add-item]])

(defn+ check-dying [character]
  "Check if character should die and process accordingly"
  (when (<= (. character hit-points) 0)
    (drop-items character)
    (when (= character character.model.player)
      (setv (. character model end-condition) *died-in-dungeon*))
    (.raise-event character (new-death-event :deceased character))
    (remove-character (. character level) character))
  character)

(defn drop-items [character]
  "drop all items of this character"
  (ap-each (. character inventory)
           (.remove (. character inventory) it)
           (add-item (. character level) (. character location) it)
           (.raise-event character (new-drop-event character it)))
  (when (. character inventory weapon)
    (add-item (. character level)
              (. character location)
              (. character inventory weapon))
    (.raise-event character (new-drop-event character (. character inventory weapon)))))

(defn+ calculate-score [character]
  "calculate score for character"
  (* (sum (list-comp (. item cost) [item (. character inventory)]))
     (cond [(= (. character model end-condition) *died-in-dungeon*) 0.75]
           [(= (. character model end-condition) *escaped-dungeon*) 1.25]
           [true 1.0])))
