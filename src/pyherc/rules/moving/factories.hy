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
(require pyherc.rules.macros)

(import [random]        
        [hymn.types.either [Left Right right?]]
        [pyherc.aspects [log-debug log-info]]
        [pyherc.data [remove-character get-portal blocks-movement get-character
                      movement-mode free-passage
                      add-character move-character add-visited-level
                      visited-levels speed-modifier]]
        [pyherc.data.constants [Duration]]
        [pyherc.data.level [traps↜]]
        [pyherc.data.geometry [find-direction area-around]]
        [pyherc.data.model [*escaped-dungeon*]]
        [pyherc.events [new-move-event new-level-event]]
        [pyherc])

(defn+ move [character direction]
  "move character to given direction"
  (if (call move-legal? character direction)
    (let [[location character.location]
          [new-level character.level]        
          [new-location nil]]
      (if (= 9 direction)
        (enter-portal-m character)
        (do
         (setv new-location (.get-location-at-direction character direction))
         (cond 
          [(both-ai-characters? (get-character new-level new-location)
                                character)
           (do (switch-places-m character direction)
               (trigger-traps-m character)
               (trigger-traps-m (get-character new-level location))
               (Right character))]
          [true (do (move-character-to-location-m character new-location new-level)
                    (trigger-traps-m character)
                    (Right character))]))))
    (do (.add-to-tick character (/ Duration.fast (speed-modifier character)))
        (Left character))))

(defn+ move-legal? [character direction]
  "is given move legal?"
  (if (= direction 9)
    true
    (let [[new-location (.get-location-at-direction character direction)]]
      (all [(is-not (. character level) nil)
            (free-passage (. character level) new-location)
            (ap-if (get-character (. character level) new-location)
                   (both-ai-characters? it character)
                   true)]))))

(defn switch-places-m [character direction]
  "make this character switch places with another in given direction"
  (let [[new-location (.get-location-at-direction character direction)]
        [another-character (get-character (. character level) new-location)]]
       (move-character-to-location-m another-character (. character location) (. character level))
       (move-character-to-location-m character new-location (. character level))))

(defn trigger-traps-m [character]
  "trigger traps for character and check if they died"
  (when (= (movement-mode character) "walk")
    (ap-each (traps↜ (. character level) (. character location))
             (.on-enter it character))
    (call check-dying character))
  (Right character))

(defn move-character-to-location-m [character location level]
  (let [[old-location character.location]
        [old-level character.level]
        [direction (find-direction old-location location)]]
    (move-character level location character)
    (.add-to-tick character (/ Duration.fast (speed-modifier character)))
    (when-not (in level (visited-levels character))
              (add-visited-level character level)
              (.raise-event character (new-level-event :character character
                                                       :new-level level)))
    (.raise-event character (new-move-event :character character
                                            :old-location old-location
                                            :old-level old-level
                                            :direction direction))
    (Right character)))

(defn enter-portal-m [character]
  "get action for entering portal"
  (let [[location character.location]
        [level character.level]
        [portal (get-portal level location)]]
    (if portal
      (if portal.exits-dungeon
        (do (setv (. character model end-condition) *escaped-dungeon*)
            (Right character))
        (let [[other-end (.get-other-end portal)]]
          (do (move-character-to-location-m character
                                            (landing-location other-end)
                                            (. other-end level))
              (trigger-traps-m character))))
      (move-character-to-location-m character location level))))

(defn both-ai-characters? [character1 character2]
  (and character1 (. character1 artificial-intelligence)
       character2 (. character2 artificial-intelligence)))

(defn landing-location [portal]
  "get landing spot on or around a portal"
  (if (not (or (blocks-movement portal.level portal.location)
               (get-character portal.level portal.location)))
    portal.location
    (.choice random (list-comp x [x (area-around portal.location)]
                               (not (or (blocks-movement portal.level x)
                                        (get-character portal.level x)))))))
