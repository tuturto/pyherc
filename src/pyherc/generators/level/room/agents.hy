;; -*- coding: utf-8 -*-

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
(require [hy.extra.anaphoric [ap-each]])

(import [pyherc.data.geometry [area-4-around distance-between]]
        [pyherc.generators.level.partitioners [section-connections
                                               match-section-to-room
                                               section-wall section-floor
                                               section-width section-height
                                               section-location-tag]]
        [random])

(defn new-tunneler-agent [floor-tile section start destination &optional [stop-at-room False]]
  "create new tunneler agent"
  (TunnelerAgent floor-tile section start destination stop-at-room))

(defn new-cave-agent [floor-tile section center size]
  "create new cave agent"
  (CaveAgent floor-tile section center (min size)))

(defn tunnels [floor-tile]
  "create old style generator for tunnels"
  (fn [section &optional trap-generator]
    "connect room and section connections together with tunnels"
    (-> (map (fn [section-connection]
               (new-tunneler-agent floor-tile
                                   section
                                   (. (.translate-to-section section-connection) location)
                                   (. (match-section-to-room section section-connection) location)))
             (section-connections section))
        (run-until-done))))

(defn wide-tunnels [floor-tile]
  "create old style generator for tunnels"
  (fn [section &optional trap-generator]
    "connect room and section connections together with tunnels"
    (-> (map (fn [section-connection]
               [(new-tunneler-agent floor-tile
                                   section
                                   (. (.translate-to-section section-connection) location)
                                   (. (match-section-to-room section section-connection) location))
                (new-tunneler-agent floor-tile
                                   section
                                   (. (.translate-to-section section-connection) location)
                                   (. (match-section-to-room section section-connection) location))])
             (section-connections section))
        (run-until-done))))

(defn cave-in-middle [floor-tile]
  "agents to create irregular cave in middle"
  (fn [section &optional trap-generator]
    (let [width (section-width section)
          height (section-height section)
          center (, (// width 2) (// height 2))
          size (, (// width 2) (// height 2))]
      (map (fn [x] (new-cave-agent floor-tile section center size))
           (range 20)))))

(defn tunnels-to-cave [corridor-tile]
  "agents to tunnel wide corridors in the middle of section"
  (fn [section &optional trap-generator]
    (map (fn [section-connection]
           [(new-tunneler-agent corridor-tile
                               section
                               (. (.translate-to-section section-connection) location)
                               (, (// (section-width section) 2)
                                  (// (section-height section) 2))
                               :stop-at-room True)
            (new-tunneler-agent corridor-tile
                               section
                               (. (.translate-to-section section-connection) location)
                               (, (// (section-width section) 2)
                                  (// (section-height section) 2))
                               :stop-at-room True)])
         (section-connections section))))

(defn agent-group [&rest agents]
  "create group for agents"
  (fn [section &optional trap-generator]
    (let [primed (flatten (map (fn [x] (x section trap-generator))
                               agents))]
      (run-until-done primed))))

(defn run-until-done [agents]
  "run agents until all of them are finished"
  (setv active-ones (list-comp agent [agent agents]
                               (not (.finished? agent))))
  (while active-ones
    (setv active-ones (run-step active-ones))))

(defn run-step [agents]
  "run agents for one step and return active agents"
  (ap-each agents (.run it))
  (list-comp agent [agent agents] (not (.finished? agent))))

(defn remove-finished [&rest agents]
  "filter out finished agents"
  (list-comp agent [agent agents]
             (not (.finished? agent))))

;; TODO: DSL eventually for defining agents?

(defclass CaveAgent []

  (defn --init-- [self floor-tile section center counter]
    (set-attributes floor-tile section center counter)
    (setv (. self location) center)
    (setv (. self first-step?) True))

  (defn run [self]
    (when (. self first-step?)
      (section-wall (. self section) (. self location) None "room")
      (section-floor (. self section) (. self location) (. self floor-tile) None)
      (setv (. self first-step?) False))
    (setv (. self location)
          (.choice random (list (area-4-around (. self location)))))
    (section-wall (. self section) (. self location) None "room")
    (section-floor (. self section) (. self location) (. self floor-tile) None)    
    (setv self.counter (dec self.counter))) 
  
  (defn finished? [self]
    (<= self.counter 0)))

(defclass TunnelerAgent []

  (defn --init-- [self floor-tile section start destination stop-at-room]
    (set-attributes floor-tile section start destination stop-at-room)
    (setv (. self location) start)
    (setv (. self first-step?) True))

  (defn run [self]
    (when (. self first-step?)
      (section-wall (. self section) (. self location) None "corridor")
      (section-floor (. self section) (. self location) (. self floor-tile) None)
      (setv (. self first-step?) False))
    
    (let [loc-dist (list-comp (, loc (distance-between loc (. self destination)))
                              [loc (area-4-around (. self location))])
          distance (distance-between (. self location) (. self destination))
          max-distance (max (list-comp (second pair) [pair loc-dist]))
          min-distance (min (list-comp (second pair) [pair loc-dist]))
          steps-towards (if (> distance 3.0)
                          (list-comp (first pair) [pair loc-dist] (not (= (second pair)
                                                                          max-distance)))
                          (list-comp (first pair) [pair loc-dist] (= (second pair)
                                                                     min-distance)))]      
      ;; TODO: avoidance logic and such
      ;; TODO: move generally towards the goal
      (if steps-towards
        (do (setv (. self location) (.choice random steps-towards))
            (section-wall (. self section) (. self location) None "corridor")
            (section-floor (. self section) (. self location) (. self floor-tile) None))
        (assert False) "no steps left to tunnel")))

  (defn finished? [self]
    
    (or (= (. self location)
           (. self destination))
        (and (. self stop-at-room)
             (in "room"
                 (section-location-tag (. self section) (. self location)))))))
