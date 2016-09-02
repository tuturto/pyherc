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

(import [random]        
        [toolz [curry]]
        [pyherc.ai [ai-state]]
        [pyherc.data [next-to-wall? corridor? doorframe? blocks-movement
                      open-area?]]
        [pyherc.data.geometry [find-direction area-4-around]]
        [pyherc.data.level [tiles↜]]
        [pyherc.ports [wait]]
        pyherc)

(defn clear-current-destination [character]
  "clear current destination of character"
  (let [[state (ai-state character)]]
    (assoc state :current-destination nil)
    (assoc state :cuurent-route nil)))

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

(defn set-current-destination [character location]
  "sets current destination"
  (let [[state (ai-state character)]]
    (assoc state :current-destination location)))

(defn set-current-route [find-path character &optional [steps nil]]
  "calculate route to a given location and set it to current route"
  (let [[state (ai-state character)]
        [#t(path connections updated) (find-path (. character location)
                                                 (:current-destination state)
                                                 (. character level))]
        [route (if steps
                 (slice path 1 steps) ;; ignore starting square
                 (slice path 1))]]
    (assoc state :current-route route)))

(defn close-in [find-path character target]
  "take one step towards given location"
  (let [[#t(path connections updated) (find-path (. character location)
                                                 target
                                                 (. character level))]
        [direction (find-direction (. character location) (second path))]]
    (if (call move-legal? character direction)
      (call move character direction)
      (wait character)))) ;; TODO: special cases and everything

(defn take-step-towards-destination [character]
  "take next step in current route"
  (let [[state (ai-state character)]
        [route (current-route character)]
        [#t(next-square new-route) #t((first route) (list (rest route)))]
        [direction (find-direction (. character location) next-square)]]
    (if (call move-legal? character direction)
      (call move character direction)
      ;; TODO: recalculate?
      (wait character))
    (assoc state :current-route new-route)))

(defn current-route [character]
  "this characers current route"
  (:current-route (ai-state character)))

(defn current-route-empty? [character]
  "has character traveled through their precalculated route?"
  (not (:current-route (ai-state character))))

(defn current-destination [character]
  "current destination of this character"
  (if (in :current-destination (ai-state character))
    (:current-destination (ai-state character))
    nil))

(defn new-destination? [character location]
  "is this completely new destination?"
  (or (is nil (current-destination character))
      (not (= (current-destination character) location))))

(defn arrived-destination? [character]
  "has character arrived to their destination"
  (= (. character location) (current-destination character)))

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

(defn along-open-space []
  "create function to return all neighbours in open space in cardinal direction"
  (fn [level location]
    (filter (fn [it]
              (and (open-area? level it)
                   (not (blocks-movement level it))))
            (area-4-around location))))

(defn fill-along-walls [level]
  "create function to use flood fill along walls"
  (fn [location]
    (filter (wallside? level)
            (area-4-around location))))

(defn fill-open-space [level]
  "create function to use flood fill in open space"
  (fn [location]
    (filter (open-area? level)
            (area-4-around location))))

(defn home-area [character]
  "home area of character"
  (if (in :home-area (ai-state character))
    (:home-area (ai-state character))
    nil))

(defn map-home-area [character neighbours]
  "build map of home area for character"
  ;; TODO: generalize to flood fill and move to geometry
  (let [[state (ai-state character)]
        [to-check [(home-location character)]]
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
    (when (or (is (current-destination character) nil)
              (= (current-destination character) (. character location)))
      (while (or (is (current-destination character) nil)
                 (= (current-destination character) (. character location)))
        (set-current-destination character (.choice random (home-area character)))))
    (travel-destination find-path character (current-destination character))))

(defn home-location [character]
  "selected home location of character"
  (if (in :home-location (ai-state character))
    (:home-location (ai-state character))
    nil))

(defn select-home [character predicate]
  "select home square for given character"
  (let [[level (. character level)]
        [candidates (list-comp location [#t(location tile) (tiles↜ level)]
                               (predicate level location))]]
    (assoc (ai-state character) :home-location (.choice random candidates))))

(with-decorator curry
  (defn wallside? [level location]
    "is given location next to wall or doorframe, but not in corridor"
    (and (or (next-to-wall? level location)
             (and (not (blocks-movement level location))
                  (any (map (doorframe? level)
                            (area-4-around location)))))
         (not (corridor? level location)))))
