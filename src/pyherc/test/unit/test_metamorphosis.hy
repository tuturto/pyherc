;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2014 Tuukka Turto
;;
;;  This file is part of pyherc.
;;
;;  pyherc is free software: you can redistribute it and/or modify
;;  it under the terms of the GNU General Public License as published by
;;  the Free Software Foundation, either version 3 of the License, or
;;  (at your option) any later version.
;;
;;  pyherc is distributed in the hope that it will be useful,
;;  but WITHOUT ANY WARRANTY; without even the implied warranty of
;;  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;  GNU General Public License for more details.
;;
;;  You should have received a copy of the GNU General Public License
;;  along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

(require hy.contrib.anaphoric)
(require pyherc.macros)
(import [pyherc.test.builders [ActionFactoryBuilder CharacterBuilder
                               LevelBuilder MetamorphosisFactoryBuilder]]
        [pyherc.data [Model add-character get-characters]]
        [pyherc.data.geometry [area-around]]
        [pyherc.rules.metamorphosis.interface [morph]]
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
                   (.with-floor-tile :floor)
                   (.with-wall-tile nil)
                   (.build))]
        [character (generator "fungi")]
        [action-factory (-> (ActionFactoryBuilder)
                            (.with-metamorphosis-factory
                             (-> (MetamorphosisFactoryBuilder)
                                 (.with-character-generator generator)
                                 (.build)))
                            (.build))]]
    (add-character level #t(5 5) character)
    {:model model
     :config config
     :generator generator
     :level level
     :character character
     :action-factory action-factory}))

(defn test-basic-metamorphosis []
  "test that character can morph to another character"
  (let [[context (setup)]
        [level (:level context)]
        [character (:character context)]
        [action-factory (:action-factory context)]]
    (morph character "fire fungi" action-factory)
    (let [[morphed-character (first (list (get-characters level)))]]
      (assert-that (count (get-characters level)) (is- (equal-to 1)))
      (assert-that morphed-character.name (is- (equal-to "fire fungi"))))))

(defn test-destroying-characters-in-metamorphosis []
  "sometimes characters around morphee are destroyed"
  (let [[context (setup)]
        [level (:level context)]
        [character (:character context)]
        [action-factory (:action-factory context)]
        [generator (:generator context)]]
    (ap-each (area-around character.location)
             (add-character level it (generator "fungi")))
    (assert-that (count (get-characters level)) (is- (equal-to 9)))
    (let [[destroyed (ap-filter (!= it character) (get-characters level))]]
      (morph character "fire fungi" action-factory destroyed))
    (assert-that (count (get-characters level)) (is- (equal-to 1)))))
