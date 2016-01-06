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
        [pyherc.ports [dig set-action-factory equip]])

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
    (.add-item configs (ItemConfiguration "dagger" 1 1 ["dagger"] ["weapon"]
                                          "common"))
    (.add-item configs (ItemConfiguration "coin" 1 1 ["coin"] [] "common"))
    (.add-item configs (ItemConfiguration "spade" 1 1 ["spade"] ["spade" "weapon"]
                                          "common"))
    (ItemGenerator configs)))

(defn configure-characters [model item-generator]
  "create character configuration for this test"
  (partial generate-creature {"skeleton" (creature-config "skeleton" 1 1 1 1 1
                                                          ["icons"] 1)
                                         "pete" (creature-config "pete" 1 1 1 1 1 ["icons"]
                                                                 1)}
           model item-generator (Random)))

(defn setup[]
  (let [[model (Model)]
        [level (-> (LevelBuilder)
                   (.with-size #t(30 20))
                   (.with-floor-tile "floor")
                   (.with-wall-tile nil)
                   (.with-model model)
                   (.build))]
        [partitioner (grid-partitioning #t(10 10) 2 1 (Random))]
        [sections (partitioner level)]
        [item-generator (configure-items)]
        [character-generator (configure-characters model item-generator)]
        [generator (LibraryRoomGenerator "floor" "corridor" nil "grave" 100 
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
    (set-action-factory action-factory)
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
    (dig character)
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
    (equip character spade)
    (assert character.inventory.weapon)
    (dig character)
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
    (equip character dagger)
    (dig character)
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
    (equip character spade)
    (dig character)
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
    (equip character spade)
    (dig character)
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
    (equip character spade)
    (dig character)))
