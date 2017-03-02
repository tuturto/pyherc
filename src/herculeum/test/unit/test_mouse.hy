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

(require [pyherc.macros [*]]
         [archimedes [fact background with-background]])

(import [hamcrest [assert-that is- equal-to]]
        [PyQt4.QtCore [Qt]]
        [herculeum.ui.gui.mouse [move?]]
        [pyherc.data [add-character]]
        [pyherc.ports [equip]]
        [pyherc.test.builders [LevelBuilder CharacterBuilder ItemBuilder]]
        [pyherc.test.matchers [falsy? truthy?]])

(background unarmed-scenario
            level (-> (LevelBuilder)
                      (.build))
            character (-> (CharacterBuilder)
                          (.build))
            close-enemy (-> (CharacterBuilder)
                            (.build))
            far-enemy (-> (CharacterBuilder)
                          (.build))
            _ (add-character level #t(5 5) character)
            _ (add-character level #t(5 6) close-enemy)
            _ (add-character level #t(2 2) far-enemy))

(background melee-scenario
            level (-> (LevelBuilder)
                      (.build))
            character (-> (CharacterBuilder)
                          (.build))
            sword (-> (ItemBuilder)
                      (.with-name "dagger")
                      (.with-damage 2 "piercing"))
            close-enemy (-> (CharacterBuilder)
                            (.build))
            far-enemy (-> (CharacterBuilder)
                          (.build))
            _ (add-character level #t(5 5) character)
            _ (add-character level #t(5 6) close-enemy)
            _ (add-character level #t(2 2) far-enemy)
            _ (equip character sword))

(background ranged-scenario
            level (-> (LevelBuilder)
                      (.build))
            character (-> (CharacterBuilder)
                          (.build))
            bow (-> (ItemBuilder)
                    (.with-name "bow")
                    (.with-required-ammunition-type "arrow")
                    (.build))
            arrows (-> (ItemBuilder)
                       (.with-name "arrow")
                       (.with-ammunition-type "arrow")
                       (.build))
            far-enemy (-> (CharacterBuilder)
                          (.build))
            untargetable-enemy (-> (CharacterBuilder)
                                   (.build))
            adjacent-enemy (-> (CharacterBuilder)
                               (.build))
            _ (add-character level #t(5 5) character)
            _ (add-character level #t(10 5) far-enemy)
            _ (add-character level #t(10 7) untargetable-enemy)
            _ (add-character level #t(4 5) adjacent-enemy)
            _ (equip character bow)
            _ (equip character arrows))

(fact "clicking empty square doesn't move character"
      (with-background unarmed-scenario [character]
        (assert-that (move? (left-click) character #t(1 1))
                     (is- (falsy?)))))

(fact "clicking enemy while unarmed next to you doesn't move character"
      (with-background unarmed-scenario [character close-enemy]
        (assert-that (move? (left-click) character close-enemy.location)
                     (is- (falsy?)))))

(fact "clicking enemy far away while using unarmed combat moves character"
      (with-background unarmed-scenario [character far-enemy]
        (assert-that (move? (left-click) character far-enemy.location)
                     (is- (truthy?)))))

(fact "clicking enemy while using melee combat next to you doesn't move character"
      (with-background melee-scenario [character close-enemy]
        (assert-that (move? (left-click) character close-enemy.location)
                     (is- (falsy?)))))

(fact "clicking enemy far away while using melee combat moves character"
      (with-background melee-scenario [character sword far-enemy]
        (assert-that (move? (left-click) character far-enemy.location)
                     (is- (truthy?)))))

(fact "clicking enemy far away and out of straight line in ranged combat moves character"
      (with-background ranged-scenario [character untargetable-enemy]
        (assert-that (move? (left-click) character untargetable-enemy.location)
                     (is- (truthy?)))))

(fact "clicking enemy far away but in straight in ranged combat line doesn't move character"
      (with-background ranged-scenario [character far-enemy]
        (assert-that (move? (left-click) character far-enemy.location)
                     (is- (falsy?)))))

(fact "clicking adjacent enemy in ranged combat doesn't move character"
      (with-background ranged-scenario [character adjacent-enemy]
        (assert-that (move? (left-click) character adjacent-enemy.location)
                     (is- (falsy?)))))

(defclass left-click []
  "helper class to simulate left click"
  []

  (defn --init-- [self])

  (defn button [self]
    Qt.LeftButton))
