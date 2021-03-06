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

(require [pyherc.aspects [*]])
(require [pyherc.macros [*]])
(require [herculeum.ai.macros [*]])

(import [pyherc.aspects [log_debug]]
        [pyherc.data.geometry [find-direction]]    
        [pyherc.events [new-notice-event]]
        [math [sqrt]]
        pyherc)

#d(defn wait [ai]
    "make character to wait a little bit"
    (setv ai.character.tick 5))

#d(defn can-walk? [ai action-factory direction]
    "check if character can walk to given direction"
    (call move-legal? ai.character direction))

#d(defn walk [ai action-factory &optional direction]
    "take a step to direction the ai is currently moving"
    (if direction
      (call move ai.character direction)
      (call move ai.character (second ai.mode))))

(defn distance-between [start end]
  "calculate distance between two locations"
  (let [dist-x (- (first start) (first end))
        dist-y (- (second start) (second end))]
    (sqrt (+ (pow dist-x 2)
	     (pow dist-y 2)))))

#d(defn new-location [character direction]
    "get next location if going to given direction"
    (.get-location-at-direction character direction))

#d(defn attack-enemy [ai enemy action-factory rng]
    "attack an enemy"
    (let [attacker ai.character
          attacker-location attacker.location
          target-location enemy.location
          attack-direction (find-direction attacker-location target-location)]
      (call attack attacker attack-direction)))

#d(defn focus-enemy [ai enemy]
    "focus on enemy and start tracking it"
    (let [character ai.character
          event (new-notice-event character enemy)]
      (.raise-event character event)))
