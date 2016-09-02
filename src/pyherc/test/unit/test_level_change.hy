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

(import [hamcrest [assert-that is- equal-to has-item]]
        [mockito [mock verify verifyNoMoreInteractions]])
(import [pyherc.test.builders [ActionFactoryBuilder CharacterBuilder
                               LevelBuilder]]
        [pyherc.test.matchers [EventType]])
(import [pyherc.data [add-visited-level]]
        [pyherc.data.new-character [visited-levels↜]]
        [pyherc.data.constants [Direction]]
        [pyherc.ports [set-action-factory]]
        pyherc)

(defn test-add-visited-level []
  "test that adding and retrieving a level in visited list is possible"
  (let [[character (-> (CharacterBuilder)
                       (.build))]]
    (add-visited-level character "crystal forest")
    (assert-that (visited-levels↜ character)
                 (has-item "crystal forest"))))

(defn test-same-level-added-only-once []
  "test that same level can be added only once"
  (let [[character (-> (CharacterBuilder)
                       (.build))]]
    (add-visited-level character "crystal forest")
    (add-visited-level character "crystal forest")
    (assert-that (len (list (visited-levels↜ character)))
                 (is- (equal-to 1)))))

(defn setup []
  "setup test case"
  (let [[listener (mock)]
        [character (-> (CharacterBuilder)
                       (.with-update-listener listener)
                       (.build))]
        [level (-> (LevelBuilder)
                   (.with-character character #t(5 5))
                   (.build))]        
        [actions (-> (ActionFactoryBuilder)
                     (.build))]]
    (set-action-factory actions)
    {:listener listener
     :level level
     :character character}))

(defn test-event-raised []
  "moving to new level should raise new level event"
  (let [[context (setup)]
        [listener (:listener context)]
        [level (:level context)]
        [character (:character context)]]
    (call move character Direction.north)
    (-> (verify listener)
        (.receive-update (EventType "new level")))))

(defn test-event-not-raised-for-old-level []
  "when player moves in an old level, no new level event should be raised"
  (let [[context (setup)]
        [listener (:listener context)]
        [level (:level context)]
        [character (:character context)]]
    (add-visited-level character level)
    (call move character Direction.north)
    (-> (verify listener)
        (.receive-update (EventType "move")))
    (verifyNoMoreInteractions listener)))
