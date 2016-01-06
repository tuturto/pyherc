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
(import [pyherc.test.builders [ActionFactoryBuilder CharacterBuilder
                               LevelBuilder MetamorphosisFactoryBuilder]]
        [pyherc.data [Model add-character get-characters]]
        [pyherc.data.geometry [area-around]]
        [pyherc.ports [morph set-action-factory]]
        [pyherc.generators [generate-creature creature-config]]
        [hamcrest [assert-that is- equal-to]]
        [functools [partial]]
        [random [Random]])


(defn setup []
  "setup test cases"
  (let [[model (Model)]
        [config {"fungi" (creature-config "fungi" 7 2 1 12 2 nil 2)
                         "fire fungi" (creature-config "fire fungi" 7 2 1 12 2 nil 2)}]
        [generator (partial generate-creature
                            config
                            model
                            nil
                            (Random))]
        [level (-> (LevelBuilder)
                   (.with-floor-tile "floor")
                   (.with-wall-tile nil)
                   (.build))]
        [character (generator "fungi")]
        [action-factory (-> (ActionFactoryBuilder)
                            (.with-metamorphosis-factory
                             (-> (MetamorphosisFactoryBuilder)
                                 (.with-character-generator generator)
                                 (.build)))
                            (.build))]]
    (set-action-factory action-factory)
    (add-character level #t(5 5) character)
    {:model model
     :config config
     :generator generator
     :level level
     :character character}))

(defn test-basic-metamorphosis []
  "test that character can morph to another character"
  (let [[context (setup)]
        [level (:level context)]
        [character (:character context)]]
    (morph character "fire fungi")
    (let [[morphed-character (first (list (get-characters level)))]]
      (assert-that (count (get-characters level)) (is- (equal-to 1)))
      (assert-that morphed-character.name (is- (equal-to "fire fungi"))))))

(defn test-destroying-characters-in-metamorphosis []
  "sometimes characters around morphee are destroyed"
  (let [[context (setup)]
        [level (:level context)]
        [character (:character context)]
        [generator (:generator context)]]
    (ap-each (area-around character.location)
             (add-character level it (generator "fungi")))
    (assert-that (count (get-characters level)) (is- (equal-to 9)))
    (let [[destroyed (ap-filter (!= it character) (get-characters level))]]
      (morph character "fire fungi" destroyed))
    (assert-that (count (get-characters level)) (is- (equal-to 1)))))
