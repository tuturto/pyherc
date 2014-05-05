;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2014 Tuukka Turto
;;
;;   This file is part of pyherc.
;;
;;   pyherc is free software: you can redistribute it and/or modify
;;   it under the terms of the GNU General Public License as published by
;;   the Free Software Foundation, either version 3 of the License, or
;;   (at your option) any later version.
;;
;;   pyherc is distributed in the hope that it will be useful,
;;   but WITHOUT ANY WARRANTY; without even the implied warranty of
;;   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;   GNU General Public License for more details.
;;
;;   You should have received a copy of the GNU General Public License
;;   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

(require hy.contrib.anaphoric)
(require pyherc.macros)
(import [pyherc.test.builders [ActionFactoryBuilder CharacterBuilder
			       LevelBuilder MitosisFactoryBuilder]]
	[pyherc.data [Model]]
	[pyherc.data.geometry [distance-between area-around]]
	[pyherc.rules.mitosis.interface [perform-mitosis]]
	[pyherc.generators [generate-creature creature-config]]
	[hamcrest [assert-that is- equal-to less-than greater-than-or-equal-to
		   all-of]]
	[functools [partial]]
	[random [Random]])

(defn setup []
  (let [[model (Model)]
	[config {"fungi" (creature-config "fungi" 7 2 1 12 2 nil 2)}]
	[generator (partial generate-creature
			    config
			    model
			    nil
			    (Random))]
	[level (-> (LevelBuilder)
		   (.with-floor-tile :floor)
		   (.with-wall-tile nil)
		   (.with-empty-wall-tile nil)
		   (.build))]
	[character (generator "fungi")]
	[action-factory (-> (ActionFactoryBuilder)
			    (.with-mitosis-factory
			     (-> (MitosisFactoryBuilder)
				 (.with-character-generator generator)
				 (.build)))
			    (.build))]]
    (.add-creature level character #t(5 5))
    {:model model
     :config config
     :generator generator
     :level level
     :character character
     :action-factory action-factory}))

(defn test-character-can-duplicate []
  (let [[context (setup)]
	[level (:level context)]
	[character (:character context)]
	[action-factory (:action-factory context)]]
    (perform-mitosis character action-factory)
    (assert-that (len level.creatures) (is- (equal-to 2)))))

(defn test-new-character-is-generated-next-to-old-one []
  (let [[context (setup)]
	[level (:level context)]
	[character (:character context)]
	[action-factory (:action-factory context)]]
    (perform-mitosis character action-factory)
    (let [[character₀ (first level.creatures)]
	  [character₁ (second level.creatures)]
	  [distance (distance-between character₀ character₁)]]
      (assert-that distance (is- (less-than 2)))
      (assert-that distance (is- (greater-than-or-equal-to 1))))))

(defn test-new-character-is-not-generated-on-top-of-old-ones []
  (let [[context (setup)]
	[level (:level context)]
	[character (:character context)]
	[action-factory (:action-factory context)]
	[generator (:generator context)]
	[surrounding-tiles (area-around character.location)]]
    (ap-each surrounding-tiles (let [[new-character (generator "fungi")]]
				 (.add-creature level new-character it)))
    (perform-mitosis character action-factory)
    (assert-that (len level.creatures) (is- (equal-to 9)))))
