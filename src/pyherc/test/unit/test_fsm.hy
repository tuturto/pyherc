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

(require [archimedes [*]])
(require [pyherc.fsm [*]])

(import [hamcrest [assert-that is- equal-to has-items]])

(defstatemachine SimpleAdder [message]

  "add 1 to message, 0 to switch state"
  (addition initial-state
            (active (+ message 1))
            (transitions [(= message 0) subtraction]))

  "substract 1 from message, 0 to switch state"
  (subtraction (active (- message 1))
               (transitions [(= message 0) addition])))

(background simple
            fsm (SimpleAdder))

(fact "fsm - calling simple adder with 2 will return 3"
      (with-background simple [fsm]
        (assert-that (fsm 2) (is- (equal-to 3)))))

(fact "fsm - incorrect element is reported"
      (assert-macro-error "unknown form"
                          (defstatemachine IncorrectElement [message]
                            (do-stuff initial-state-2
                                      (active message)))))

(fact "fsm - calling simple adder with 0 will switch state"
      (with-background simple [fsm]
        (assert-that (fsm 0) (is- (equal-to -1)))))

(fact "fsm - simple adder - state transition and message processing works"
      (with-background simple [fsm]
        (fsm 0)
        (assert-that (fsm 5) (is- (equal-to 4)))))

(fact "fsm - simple adder - multiple transitions work"
      (with-background simple [fsm]
        (fsm 0)
        (fsm 0)
        (assert-that (fsm 5) (is- (equal-to 6)))))



(defstatemachine TwistedAccumulator [message]
  "twisted accumulator demonstrates shared state"

  "add bonus to message"
  (addition initial-state
            (on-activate (state bonus 0))
            (active (when (odd? message)
                      (state bonus message))
                    (+ message (state bonus)))
            "send 0 to transition to subtraction"
            (transitions [(= message 0) subtraction]))

  "substract bonus from message"
  (subtraction (active (when (odd? message) 
                         (state bonus message))
                       (- message (state bonus)))
               "send 0 to transition to addition"
               (transitions [(= message 0) addition])))

(background twister
            fsm (TwistedAccumulator))

(fact "fsm - twisted - state can be modified"
      (with-background twister [fsm]
        (assert-that (fsm 2) (is- (equal-to 2)))
        (assert-that (fsm 1) (is- (equal-to 2)))
        (assert-that (fsm 2) (is- (equal-to 3)))
        (assert-that (fsm 3) (is- (equal-to 6)))))



(defstatemachine Minimal [message]
  "default initializer"
  (--init-- [bonus] (state bonus bonus))
  "handle message"
  (process initial-state
           (active (* message (state bonus)))))

(background minimal
            fsm (Minimal 2))

(fact "finite-state machine can be configured during construction"
      (with-background minimal [fsm]
        (assert-that (fsm 2) (is- (equal-to 4)))))


(defstatemachine Transitions [message]
  "state machine for testing transitions"
  
  (--init-- [feedback] (state feedback feedback))

  (state-1 initial-state
           (on-activate (.append (state feedback) "state-1 on activate"))
           (active message)
           (on-deactivate (.append (state feedback) "state-1 on deactivate"))
           (transitions [(= message "state-2") state-2]))

  (state-2 (on-activate (.append (state feedback) "state-2 on activate"))
           (active message)
           (on-deactivate (.append (state feedback) "state-2 on deactivate"))
           (transitions [(= message "state-1" state-1)])))

(background transition-bkg
            feedback []
            fsm (Transitions feedback))

(fact "state can have on-activate and on-deactivate handlers"
      (with-background transition-bkg [feedback fsm]
        (fsm "state-2")
        (assert-that feedback (has-items "state-1 on activate"
                                         "state-1 on deactivate"
                                         "state-2 on activate"))))
