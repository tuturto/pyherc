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
(require pyherc.fsm)
(import [random]
        [herculeum.ai.patrol [patrol-ai]]
        [pyherc.ai.pathfinding [a-star]]
        [pyherc.data [next-to-wall? corridor? blocks-movement]]
        [pyherc.data.geometry [find-direction free-locations-around
                               area-4-around]]
        [pyherc.data.level [tiles↜]]
        [pyherc.ports [wait move move-legal?]])

(defn whole-level []
  "create function to return all neighbours in cardinal directions"
  (fn [level location]
    (filter (fn [it]
              (not (blocks-movement level it)))
            (area-4-around location))))

(defn along-walls []
  "create function to return all neighbours along walls in cardinal directions"
  (fn [level location]
    (filter (fn [it]
              (and (wallside? level it)
                   (not (blocks-movement level it))))
            (area-4-around location))))

(defn fill-along-walls [level]
  "create function to use flood fill along walls"
  (fn [location]
    (filter (fn [it] 
              (wallside? level it))
            (area-4-around location))))

(defstatemachine RatAI [model action-factory rng]
  "AI routine for rats"
  (--init-- [character] (state character character))

  "first find a place to call a home"
  (finding-home initial-state
                (on-activate (select-home character wallside?))
                (active (travel-home (a-star (whole-level)) character))
                (transitions [(arrived-destination? character) patrolling]
                             [(enemy-detected? character) fighting]))
  
  "patrol alongside the walls"
  (patrolling (on-activate (map-home-area character
                                          (fill-along-walls (. character level)))
                           (clear-current-destination character))
              (active (patrol-home-area (a-star (along-walls)) character))
              (transitions [(enemy-detected? character) fighting]))
  
  "fight enemy"
  (fighting (on-activate (clear-current-destination character))
            (active (wait character))
            (on-deactivate nil)
            (transitions [(not (enemy-detected? character)) finding-home])))

(defn clear-current-destination [character]
  "clear current destination of character"
  (let [[state (ai-state character)]]
    (assoc state :current-destination nil)
    (assoc state :cuurent-route nil)))

(defn map-home-area [character neighbours]
  "build map of home area for character"
  ;; TODO: generalize to flood fill and move to geometry
  (let [[state (ai-state character)]
        [to-check [(:home-location state)]]
        [result []]]
    (while to-check
      (let [[it (.pop to-check)]]
        (when (not (in it result))
          (.append result it)
          (.extend to-check (neighbours it)))))
    (assoc state :home-area result)))

(defn patrol-home-area [find-path character]
  "move around home area"
  (let [[state (ai-state character)]]
    (when (or (is (:current-destination state) nil)
              (= (:current-destination state) (. character location)))
      (while (or (is (:current-destination state) nil)
                 (= (:current-destination state) (. character location)))
        (set-current-destination character (.choice random (:home-area state)))))
    (travel-destination find-path character (:current-destination state))))

(defn travel-home [find-path character]
  "travel towards :home-location"
  (travel-destination find-path character (:home-location (ai-state character))))

(defn travel-destination [find-path character location]
  "travel towards given location"
  (let [[state (ai-state character)]]
    (cond [(new-destination? character location)
           (do (set-current-destination character location)
               (set-current-route find-path character 10)
               (take-step-towards-destination character))]
          [(current-route-empty? character)
           (do (set-current-route find-path character)
               (take-step-towards-destination character))]
          [true 
           (take-step-towards-destination character)])))

;; take step should take into account possible obstacles

(defn set-current-destination [character location]
  "sets current destination"
  (let [[state (ai-state character)]]
    (assoc state :current-destination location)))

(defn set-current-route [find-path character &optional [steps nil]] ;; TODO: neighbours selector
  "calculate route to a given location and set it to current route"
  (let [[state (ai-state character)]
        [#t(path connections updated) (find-path (. character location)
                                                 (:current-destination state)
                                                 (. character level))]
        [route (if steps
                 (slice path 1 steps) ;; ignore starting square
                 (slice path 1))]]
    (assoc state :current-route route)))

(defn take-step-towards-destination [character]
  "take next step in :current-route"
  (let [[state (ai-state character)]
        [route (:current-route state)]
        [#t(next-square new-route) #t((first route) (list (rest route)))]
        [direction (find-direction (. character location) next-square)]]
    (if (move-legal? character direction)
      (move character direction)
      ;; TODO: recalculate?
      (wait character))
    (assoc state :current-route new-route)))

(defn current-route-empty? [character]
  "has character traveled through their precalculated route?"
  (not (:current-route (ai-state character))))

(defn new-destination? [character location]
  "is this completely new destination?"
  (let [[state (ai-state character)]]
    (or (not (in :current-destination state))
        (is nil (:current-destination state))
        (not (= (:current-destination state) location)))))

(defn arrived-destination? [character]
  "has character arrived to their destination"
  (let [[state (ai-state character)]
        [destination (if (in :current-destination state)
                       (:current-destination state)
                       nil)]]
    (= (. character location) destination)))

(defn enemy-detected? [character]
  "has AI detected an enemy"
  false)

(defn ai-state [character]
  "get state of ai"
  (. character artificial-intelligence data))

(defn select-home [character predicate]
  "select home square for given character"
  (when (not (in :home-location (ai-state character)))
    (let [[level (. character level)]
          [candidates (list-comp location [#t(location tile) (tiles↜ level)]
                                 (predicate level location))]]
      (assoc (ai-state character) :home-location (.choice random candidates)))))

(defn wallside? [level location]
  "is given location next to wall, but not in corridor"
  (and (next-to-wall? level location)
       (not (corridor? level location))))

(defclass RatAI-old []
  [[__doc__ "AI routine for rats"]
   [character None]
   [mode ["transit" None]]
   [--init-- (fn [self character]
           "default constructor"
           (.--init-- (super RatAI self))
           (setv self.character character) None)]
   [act (fn [self model action-factory rng]
      "check the situation and act accordingly"
      (rat-act self model action-factory))]])

(defn patrol-area? [level location]
  "rats prefer rooms"
  (and (next-to-wall? level location)
       (not (corridor? level location))))

(def rat-act (patrol-ai patrol-area? 4))
