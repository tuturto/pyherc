;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2015 Tuukka Turto
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

(import [functools [partial]]
        [random [Random]])
(import [hamcrest [assert-that is- equal-to]])
(import [pyherc.data [add-location-feature get-tiles location-features
                      add-character get-characters get-items Model]]
        [pyherc.data.features [new-cache items-in-cache characters-in-cache]]
        [pyherc.generators [ItemGenerator ItemConfiguration ItemConfigurations
                            creature-config generate-creature]]
        [pyherc.generators.level.partitioners [grid-partitioning]]
        [pyherc.generators.level.room [LibraryRoomGenerator]]
        [pyherc.test.builders [ActionFactoryBuilder LevelBuilder ItemBuilder
                               CharacterBuilder]]
        [pyherc.rules.inventory.interface [equip]]
        [pyherc.rules.digging [dig]])

(defn full-grave [item-generator character-generator]
  "creates a full grave in given location"
  (fn [level location]
    (add-location-feature level
                          location
                          (new-cache level location 
                                     [(.generate-item item-generator "coin")] 
                                     [(character-generator "skeleton")]))))

(defn find-feature [level]
  "find a grave"
  (for [#t(location tile) (get-tiles level)]
    (yield-from (location-features level location))))

(defn configure-items []
  "create item configuration for this test"
  (let [[configs (ItemConfigurations (Random))]]
    (.add-item configs (ItemConfiguration "dagger" 1 1 [:dagger] ["weapon"]
                                          "common"))
    (.add-item configs (ItemConfiguration "coin" 1 1 [:coin] [] "common"))
    (.add-item configs (ItemConfiguration "spade" 1 1 [:spade] [:spade "weapon"]
                                          "common"))
    (ItemGenerator configs)))

(defn configure-characters [model item-generator]
  "create character configuration for this test"
  (partial generate-creature {"skeleton" (creature-config "skeleton" 1 1 1 1 1
                                                          [:icons] 1)
                              "pete" (creature-config "pete" 1 1 1 1 1 [:icons]
                                                      1)}
           model item-generator (Random)))

(defn setup[]
  (let [[model (Model)]
        [level (-> (LevelBuilder)
                   (.with-size #t(30 20))
                   (.with-floor-tile :floor)
                   (.with-wall-tile nil)
                   (.with-model model)
                   (.build))]
        [partitioner (grid-partitioning #t(10 10) 2 1 (Random))]
        [sections (partitioner level)]
        [item-generator (configure-items)]
        [character-generator (configure-characters model item-generator)]
        [generator (LibraryRoomGenerator :floor :corridor nil :grave 100 
                                         (full-grave item-generator
                                                     character-generator)
                                         ["test"])]
        [action-factory (-> (ActionFactoryBuilder)
                            (.with-inventory-factory)
                            (.with-dig-factory)
                            (.build))]
        [character (character-generator "pete")]
        [spade (.generate-item item-generator "spade")]
        [dagger (.generate-item item-generator "dagger")]]
    (ap-each sections (.generate-room generator it))
    (.append character.inventory spade)
    (.append character.inventory dagger)
    {:level level
     :sections sections
     :grave (first (list (find-feature level)))
     :action-factory action-factory
     :character character
     :spade spade
     :dagger dagger}))

(defn test-looting-without-implement []
  "looting a grave without implement is not possible"
  (let [[context (setup)]
        [level (:level context)]
        [grave (:grave context)]
        [action-factory (:action-factory context)]
        [character (:character context)]]
    (add-character level (:location grave) character)
    (dig character action-factory)
    (assert-that (count (items-in-cache grave)) (is- (equal-to 1)))
    (assert-that (count (characters-in-cache grave)) (is- (equal-to 1)))))

(defn test-looting-with-spade []
  "looting grave with spade empties it"
  (let [[context (setup)]
        [level (:level context)]
        [grave (:grave context)]
        [action-factory (:action-factory context)]
        [character (:character context)]
        [spade (:spade context)]]
    (add-character level (:location grave) character)
    (equip character spade action-factory)
    (assert character.inventory.weapon)
    (dig character action-factory)
    (assert-that (count (items-in-cache grave)) (is- (equal-to 0)))
    (assert-that (count (characters-in-cache grave)) (is- (equal-to 0)))))

(defn test-looting-with-dagger []
  "looting is not possible with a regular weapon"
  (let [[context (setup)]
        [level (:level context)]
        [grave (:grave context)]
        [action-factory (:action-factory context)]
        [character (:character context)]
        [dagger (:dagger context)]]
    (add-character level (:location grave) character)
    (equip character dagger action-factory)
    (dig character action-factory)
    (assert-that (count (items-in-cache grave)) (is- (equal-to 1)))
    (assert-that (count (characters-in-cache grave)) (is- (equal-to 1)))))

(defn test-items-are-unearthed []
  "items from grave are unearthed after succesfull exhuming"
  (let [[context (setup)]
        [level (:level context)]
        [grave (:grave context)]
        [action-factory (:action-factory context)]
        [character (:character context)]
        [spade (:spade context)]]
    (add-character level (:location grave) character)
    (equip character spade action-factory)
    (dig character action-factory)
    (assert-that (count (get-items level)) (is- (equal-to 1)))))

(defn test-character-are-unearthed []
  "characters from grave are unearthed after succesfull exhuming"
  (let [[context (setup)]
        [level (:level context)]
        [grave (:grave context)]
        [action-factory (:action-factory context)]
        [character (:character context)]
        [spade (:spade context)]]
    (add-character level (:location grave) character)
    (equip character spade action-factory)
    (dig character action-factory)
    (assert-that (count (get-characters level)) (is- (equal-to 2)))))

(defn test-trying-to-exhume-without-grave []
  "digging somewhere else than on grave doesn't crash"
  (let [[context (setup)]
        [level (:level context)]
        [grave (:grave context)]
        [action-factory (:action-factory context)]
        [character (:character context)]
        [spade (:spade context)]
        [#t(loc_x loc_y) (:location grave)]]
    (add-character level #t((+ loc_x 1) loc_y) character)
    (equip character spade action-factory)
    (dig character action-factory)))
