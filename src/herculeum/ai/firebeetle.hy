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
        [herculeum.ai.movement [home-location select-home wallside?
                                travel-home whole-level arrived-destination?
                                map-home-area home-area fill-open-space
                                clear-current-destination patrol-home-area
                                close-in along-open-space]]
        [herculeum.ai.combat [select-current-enemy current-enemy closest-enemy
                              melee detected-enemies]]
        [pyherc.data [open-area?]]
        [pyherc.data.geometry [in-area area-4-around]]
        [pyherc.ai [a-star :as a* show-alert-icon show-confusion-icon]])

(defstatemachine FireBeetleAI []
  "AI routine for fire beetles"
  (--init-- [character] (state character character))

  "find a place to call a home"
  (finding-home initial-state
                (on-activate (when (not (home-location character))
                               (select-home character open-area?)))
                (active (travel-home (a* (whole-level)) character))
                (transitions [(arrived-destination? character) patrolling]
                             [(detected-enemies character) fighting]))
  
  "patrol middle of room"
  (patrolling (on-activate (when (not (home-area character))
                             (map-home-area character
                                            (fill-open-space (. character level)))) 
                           (clear-current-destination character))
              (active (patrol-home-area (a* (along-open-space)) character))
              (transitions [(detected-enemies character) fighting]))
  
  "fight enemy"
  (fighting (on-activate (clear-current-destination character)
                         (select-current-enemy character closest-enemy)
                         (show-alert-icon character (current-enemy character)))
            (active (if (in-area area-4-around (. character location) 
                                 (. (current-enemy character) location))
                      (melee character (current-enemy character))
                      (close-in (a* (whole-level)) 
                                character 
                                (. (current-enemy character) location))))
            (on-deactivate (show-confusion-icon character))
            (transitions [(not (detected-enemies character)) finding-home])))
