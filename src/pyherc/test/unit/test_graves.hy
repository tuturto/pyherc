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

(import [random [Random]])
(import [hamcrest [assert-that is- equal-to]])
(import [pyherc.data [add-location-feature get-tiles location-features
                      add-character get-characters]]
        [pyherc.data.features [new-grave items-in-grave characters-in-grave]]
        [pyherc.generators.level.partitioners [GridPartitioner]]
        [pyherc.generators.level.room [LibraryRoomGenerator]]
        [pyherc.test.builders [ActionFactoryBuilder LevelBuilder ItemBuilder
                               CharacterBuilder]]
        [pyherc.rules.inventory.interface [equip]]
        [pyherc.rules.exhuming [exhume]])

(defn full-grave [level location]
  "creates a full grave in given location"
  (add-location-feature level
                        location
                        (new-grave level location 
                                   [(-> (ItemBuilder)
                                        (.with-name "coin")
                                        (.build))] 
                                   [(-> (CharacterBuilder)
                                        (.with-name "skeleton")
                                        (.build))])))

(defn find-feature [level]
  "find a grave"
  (for [#t(location tile) (get-tiles level)]
    (yield-from (location-features level location))))

(defn setup[]
  (let [[level (-> (LevelBuilder)
                   (.with-size #t(30 20))
                   (.with-floor-tile :floor)
                   (.with-wall-tile nil)
                   (.build))]
        [partitioner (GridPartitioner ["test"] 2 1 (Random))]
        [sections (.partition-level partitioner level)]
        [generator (LibraryRoomGenerator :floor :corridor nil :grave 100 
                                         full-grave
                                         ["test"])]
        [action-factory (-> (ActionFactoryBuilder)
                            (.with-inventory-factory)
                            (.with_exhume-factory)
                            (.build))]]
    (ap-each sections (.generate-room generator it))
    {:level level
     :sections sections
     :grave (first (list (find-feature level)))
     :action-factory action-factory}))

(defn test-looting-without-implement []
  "looting a grave without implement is not possible"
  (let [[context (setup)]
        [level (:level context)]
        [grave (:grave context)]
        [action-factory (:action-factory context)]
        [character (-> (CharacterBuilder)
                       (.with-name "Pete")
                       (.build))]]
    (add-character level (:location grave) character)
    (exhume character action-factory)
    (assert-that (count (items-in-grave grave)) (is- (equal-to 1)))
    (assert-that (count (characters-in-grave grave)) (is- (equal-to 1)))))

(defn test-looting-with-spade []
  "looting grave with spade empties it"
  (let [[context (setup)]
        [level (:level context)]
        [grave (:grave context)]
        [action-factory (:action-factory context)]
        [character (-> (CharacterBuilder)
                       (.with-name "Pete")
                       (.build))]
        [spade (-> (ItemBuilder)
                   (.with-name "spade")
                   (.with_damage 1 "crushing")
                   (.with-tag :spade)
                   (.build))]]
    (add-character level (:location grave) character)
    (.append character.inventory spade)
    (equip character spade action-factory)
    (exhume character action-factory)
    (assert-that (count (items-in-grave grave)) (is- (equal-to 0)))
    (assert-that (count (characters-in-grave grave)) (is- (equal-to 0)))))

(defn test-looting-with-dagger []
  "looting is not possible with a regular weapon"
  (let [[context (setup)]
        [level (:level context)]
        [grave (:grave context)]
        [action-factory (:action-factory context)]
        [character (-> (CharacterBuilder)
                       (.with-name "Pete")
                       (.build))]
        [dagger (-> (ItemBuilder)
                    (.with-name "dagger")
                    (.with_damage 1 "piercing")
                    (.build))]]
    (add-character level (:location grave) character)
    (.append character.inventory dagger)
    (equip character dagger action-factory)
    (exhume character action-factory)
    (assert-that (count (items-in-grave grave)) (is- (equal-to 1)))
    (assert-that (count (characters-in-grave grave)) (is- (equal-to 1)))))
