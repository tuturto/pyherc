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

(require [pyherc.macros [*]])
(require [pyherc.rules.macros [*]])
(require [hymn.dsl [*]])

(import [random]        
        [hymn.types.either [Left Right right? left?]]
        [pyherc.aspects [log-debug log-info]]
        [pyherc.data [remove-character get-portal blocks-movement get-character
                      movement-mode free-passage
                      add-character move-character add-visited-level
                      visited-levels speed-modifier
                      raise-event-m]]
        [pyherc.data.new-character [add-tick-m]]
        [pyherc.data.constants [Duration]]
        [pyherc.data.level [traps↜]]
        [pyherc.data.geometry [find-direction area-around]]
        [pyherc.data.model [*escaped-dungeon*]]
        [pyherc.events [new-move-event new-level-event]]
        [pyherc])

(defn+ move [character direction]
  "move character to given direction"
  (if (call move-legal? character direction)
    (let [location character.location
          new-level character.level        
          new-location None]
      (if (= 9 direction)
        (enter-portal-m character)
        (do
         (setv new-location (.get-location-at-direction character direction))
         (setv character₁ character)
         (setv character₂ (get-character new-level new-location))
         (cond 
          [(both-ai-characters? character₁ character₂)
           (do-monad-e [_ (switch-places-m character₁ direction)
                        _ (trigger-traps-m character₁)
                        _ (trigger-traps-m character₂)]
                       (Right character₁))]
          [True (do-monad-e [_ (move-character-to-location-m character₁
                                                             new-location
                                                             new-level)
                             _ (add-tick-m character₁ Duration.fast)
                             _ (trigger-traps-m character₁)]
                            (Right character₁))]))))
    (do-monad-e [a₁ (add-tick-m character Duration.fast)]
                (Left "moving wasn't legal"))))

(defn+ move-legal? [character direction]
  "is given move legal?"
  (if (= direction 9)
    True
    (let [new-location (.get-location-at-direction character direction)]
      (all [(is-not (. character level) None)
            (free-passage (. character level) new-location)
            (ap-if (get-character (. character level) new-location)
                   (both-ai-characters? it character)
                   True)]))))

(defn switch-places-m [character direction]
  "make this character switch places with another in given direction"
  (let [new-location (.get-location-at-direction character direction)
        another-character (get-character (. character level) new-location)]
    (move-character-to-location-m another-character (. character location) (. character level))
    (add-tick-m another-character Duration.fast)    
    (move-character-to-location-m character new-location (. character level))
    (add-tick-m character Duration.fast)))

(defn trigger-traps-m [character]
  "trigger traps for character and check if they died"
  (when (= (movement-mode character) "walk")
    (ap-each (traps↜ (. character level) (. character location))
             (.on-enter it character))
    (call check-dying character))
  (Right character))

(defn move-character-to-location-m [character location level]
  "move character to new location, process time and raise appropriate events"
  (let [old-location character.location
        old-level character.level
        direction (find-direction old-location location)]
    (monad-> (set-character-location-m character level location)             
             (add-visited-level-m level)
             (raise-event-m (new-move-event :character character
                                            :old-location old-location
                                            :old-level old-level
                                            :direction direction)))))

(defn set-character-location-m [character level location]
  "move character to new location"
  (left-if-nil [character level location]
               (move-character level location character)
               (Right character)))

(defn add-visited-level-m [character level]
  "mark level visited for a character"
  (left-if-nil [character level]
               (when-not (in level (visited-levels character))
                         (add-visited-level character level)
                         (.raise-event character (new-level-event :character character
                                                                  :new-level level)))
               (Right character)))

(defn set-end-condition-m [character condition]
  (left-if-nil [character condition]
               (setv (. character model end-condition) condition)
               (Right character)))

(defn enter-portal-m [character]
  "get action for entering portal"
  (if (is-not character None)
    (let [location character.location
          level character.level]
      (ap-if (get-portal level location)
        (if it.exits-dungeon
          (set-end-condition-m character *escaped-dungeon*)
          (let [other-end (.get-other-end it)]
            (monad-> (move-character-to-location-m character
                                                   (landing-location other-end)
                                                   (. other-end level))
                     (add-tick-m Duration.fast)
                     (trigger-traps-m))))
        (Left character)))
    (Left character)))

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
