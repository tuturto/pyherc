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

(import [pyherc.macro-utils [quote-dict HyString?]])

(defmacro defstatemachine [fsm-class fsm-interface &rest states]
  "build class definition for a finite-state machine"

  (defn new-state [symbol &optional [on-activate nil]
                   [active nil] [transitions nil]]
    "construct new state with given functions and transitions"
    (let [[on-activate-fn (if on-activate
                            `(fn [state! ~@fsm-interface]
                               "function to call when this state activates"
                               ~@on-activate)
                            `(fn [state! ~@fsm-interface]
                               "empty function as this state doesn't have on-activate code"
                               nil))]
          [active-fn (if active
                       `(fn [state! ~@fsm-interface]
                          "function to call when this state processes a message"
                          ~@active)
                       `(fn [state! ~@fsm-interface]
                          "empty function as this state doesn't have active code"
                          nil))]
          [transitions-fn (if transitions
                            `(fn [state! ~@fsm-interface]
                               "function to call when evaluating if state should change"
                               (cond ~@(ap-map `[~(first it) ~(keyword (second it))]
                                               transitions)))
                            `(fn [state! ~@fsm-interface]
                               "empty function as this state doesn't have transitions"
                               nil))]]
      `{:symbol ~(keyword symbol)
        :on-activate ~on-activate-fn
        :active ~active-fn
        :transitions ~transitions-fn}))  

  (defn create-states []
    "create states dictionary {(keyword state-symbol) state}"
    (dict-comp (keyword (first x)) 
               (create-state x)
               [x states]
               (not (HyString? x))))
  
  (defn create-state [state-def]
    "create a state from state definition"
    (setv on-activate-code nil)
    (setv active-code nil)
    (setv transitions-code nil)
    (ap-each (rest state-def) (cond [(= 'on-activate (first it))
                                     (setv on-activate-code (list (rest it)))]
                                    [(= 'active (first it))
                                     (setv active-code (list (rest it)))]
                                    [(= 'transitions (first it)) 
                                     (setv transitions-code (list (rest it)))]
                                    [(not (or (= 'initial-state it)
                                              (HyString? it)))
                                     (macro-error it "unknown form")]))
    (new-state (first state-def) on-activate-code active-code transitions-code))

  (let [[states-dict (create-states)]
        [quoted-dict (quote-dict states-dict)]
        [initial-state-key (keyword (first (first (ap-filter (= 'initial-state
                                                         (second it))
                                                      states))))]
        [initial-state-code (get states-dict initial-state-key)]]
    `(defclass ~fsm-class []
       "a finite-state machine"
       [[--init-- (fn [self]
                    "default initializer"
                    (setv (. self current-state) nil)
                    (setv (. self initial-state) ~initial-state-code)
                    (setv (. self states) ~quoted-dict)
                    (setv (. self data) {})
                    nil)]        
        
        [--call-- (fn [self ~@fsm-interface]
                    "call current state of finite-state machine"
                    (when (not (. self current-state))
                      (setv (. self current-state) (. self initial-state))
                      ((:on-activate (. self current-state)) (. self data) ~@fsm-interface))
                    (ap-if ((:transitions (. self current-state)) (. self data) ~@fsm-interface)
                           (do (setv (. self current-state)
                                     (get (. self states) it))
                               ((:on-activate (. self current-state)) (. self data) ~@fsm-interface)))
                    ((:active (. self current-state)) (. self data) ~@fsm-interface))]])))

(defmacro state [symbol &optional [value nil]]
  "access shared state symbol in finite-state machine"
  (if (not (is value nil))
    `(do (assoc state! ~(keyword symbol) ~value)
         (get state! ~(keyword symbol)))
    `(get state! ~(keyword symbol))))
