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
(require pyherc.aspects)
(import [pyherc.aspects [log-debug]])
(import [pyherc.events [HitPointsChangedEvent]])

#d(defn receive-event [character event]
    "receives an event from world and enters it into short term memory"
    (.append character.short-term-memory event)
    (ap-each character.event-listeners (.receive-event it event)))

#d(defn raise-event [character event]
    "raise event for other characters to see"
    (.raise-event character.model event)
    (.notify-update-listeners character event))

#d(defn register-event-listener [character listener]
    "register event listener"
    (.append character.event-listeners listener))

(defn hit-points [character]
  "amount of hit points a character has"
  character.hit_points)

(defn set-hit-points [character hit-points]
  "set amount of hit points a character has"
  (let [[old-hit-points character.hit_points]
	[new-hit-points hit-points]]
    (setv character.hit_points hit-points)
    (raise-event character (HitPointsChangedEvent character old-hit-points new-hit-points))))

(defn max-hp [character]
  "maximum hit points of character"
  character.max-hp)

(defn set-max-hp [character max-hp]
  "set maximum hit points of character"
  (setv character.max-hp max-hp))

(defn body [character]
  "body attribute of character"
  character.body)

(defn set-body [character body]
  "set body attribute of character"
  (setv character.body body))

(defn finesse [character]
  "finesse attribute of character"
  character.finesse)

(defn set-finesse [character finesse]
  "set finesse attribute of character"
  (setv character.finesse finesse))

(defn mind [character]
  "mind attribute of character"
  character.mind)

(defn set-mind [character mind]
  "set mind attribute of character"
  (setv character.mind mind))

(defn attack-value [character]
  "attack value of character"
  character.attack)

(defn set-attack-value [character attack-value]
  "set attack value of character"
  (setv character.attack attack-value))

#d(defn proficient-with? [character weapon]
    "check if this character is proficient with a given weapon"
    (assert weapon)
    (when (not weapon.weapon-data) true)
    (try
     (when (next (filter-matching-profincies (weapon-profincies character)
					     weapon))
       true)
     (catch [e StopIteration] false)))

(defn weapon-profincies [character]
  "get weapon profincies of a character"
  (genexpr tag [tag character.feats] (= tag.name "weapon proficiency")))

(defn filter-matching-profincies [profincies weapon]
  "get weapon profincies that match the weapon"
  (let [[weapon-data weapon.weapon-data]]
  (genexpr tag [tag profincies] 
	     (and (= tag.weapon-type weapon-data.weapon-type)
		  (or (is tag.weapon-name nil)
		      (= tag.weapon-name weapon-data.weapon-name))))))
