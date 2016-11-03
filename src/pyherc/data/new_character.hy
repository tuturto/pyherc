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

(import [pyherc.data.new-item [armour-speed-modifier boots-speed-modifier]]
        [pyherc.data.constants [sizes]]
        [hymn.types.either [Left Right]])

(defn skill-ready? [character skill]
  "check if the cooldown of a skill has passed"
  (<= (cooldown character skill) 0))

(defn cooldown [character skill &optional limit]
  "cooldown of a specific skill for a character"
  (when limit
    (assoc character.cooldowns skill limit))
  (when (not (in skill character.cooldowns))
    (assoc character.cooldowns skill 0))
  (get character.cooldowns skill))

(defn visited-levels↜ [character]
  "get generator for visited levels of this character"
  (genexpr x [x character.visited-levels]))

(defn visited-levels [character]
  "get list of visited levels for this character"
  character.visited-levels)

(defn add-visited-level [character level]
  "add level to visited levels list"
  (when (not (in level character.visited-levels))
    (.append character.visited-levels level)))

(defn speed-modifier [character]
  "get total speed modifier for this character"
  (* (armour-speed-modifier character)
     (boots-speed-modifier character)))

(defn movement-mode [character]
  "get effective movement mode, taking special items into account"
  (let [[modes (set (list-comp x.mode [x (.get-effects character)]
                               (= x.effect-name "movement mode modifier")))]]
    (if modes
      (if (in "fly" modes)
        "fly"
        "walk")
      "walk")))

(defn enemy-names [character]
  "list of names of enemies for this character"
  [])

(defn enemies [character]
  "list of enemy instances for this character"
  [])

(defn add-enemy-name [character name]
  "add new enemy name"
  (.append (. character enemy-names) name))

(defn add-enemy [character enemy]
  "add new enemy"
  (.append (. character enemies) enemy))

(defn remove-enemy-name [character name]
  "remove enemy name"
  (.remove (. character enemy-names) name))

(defn remove-enemy [character enemy]
  "remove enemy"
  (.remove (. character enemies) enemy))

(defn perception-range [character]
  "at what distance this character normally notices things"
  (ap-if (. character mind)
         (* 2 it)
         1))

(defn raise-event-m [character event]
  "raise event for character"
  (left-if-nil [character event]
               (.raise-event character event)
               (Right character)))

(defn add-tick-m [character tick]
  "add time to character's internal clock"
  (left-if-nil [character tick]
               (.add-to-tick character (/ tick (speed-modifier character)))
               (Right character)))

(defn cooldown-m [character skill &optional limit]
  "cooldown of a specific skill for a character"
  (left-if-nil [character skill]
               (when limit
                 (assoc character.cooldowns skill limit))
               (when (not (in skill character.cooldowns))
                 (assoc character.cooldowns skill 0))
               (Right (get character.cooldowns skill))))

(defn size [character &optional size]
  "size of a character"
  (when size
    (assert (in size sizes))
    (setv character.size size))
  character.size)

(defn smaller? [a b]
  "compare two sizes and check if a is smaller than b"
  (< (.index sizes a)
     (.index sizes b)))

(defn larger? [a b]
  "compare two sizes and check if a is larger than b"
  (> (.index sizes a)
     (.index sizes b)))

(defn same-size? [a b]
  "compare two sizes and check if they're same"
  (= a b))

(defn different-size? [a b]
  "compare two sizes and check if they're different"
  (not (= a b)))
