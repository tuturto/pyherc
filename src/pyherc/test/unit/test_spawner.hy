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

(import [hamcrest [assert-that has-item]]
[pyherc.data.traps [RemoteTrigger CharacterSpawner]]
        [pyherc.data.constants [Direction]]
        [pyherc.data [add-character add-trap get-characters]]
        [pyherc.ports [set-action-factory move]]
        [pyherc.test.builders [LevelBuilder CharacterBuilder
                               ActionFactoryBuilder]])

(defn setup []
  "setup test case"
  (let [[level (-> (LevelBuilder)
                   (.build))]
        [character₀ (-> (CharacterBuilder)
                        (.build))]
        [character₁ (-> (CharacterBuilder)
                        (.build))]
        [spawner (CharacterSpawner (fn [] [character₁]))]
        [trigger (RemoteTrigger spawner)]]
    (set-action-factory (-> (ActionFactoryBuilder)
                            (.with-move-factory)
                            (.build)))
    {:level level
     :spawner spawner
     :trigger trigger
     :character₀ character₀
     :character₁ character₁}))

(defn test-spawning-character []
  "character spawner can create new character on level"
  (let [[context (setup)]
        [level (:level context)]
        [character₀ (:character₀ context)]
        [character₁ (:character₁ context)]
        [spawner (:spawner context)]
        [trigger (:trigger context)]]
    (add-character level #t(1 1) character₀)
    (add-trap level #t(2 1) trigger)
    (add-trap level #t(5 5) spawner)
    (move character₀ Direction.east)
    (assert-that (list (get-characters level))
                 (has-item character₁))))
