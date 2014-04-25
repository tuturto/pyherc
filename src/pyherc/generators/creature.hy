;; -*- coding: utf-8 -*-

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
(require pyherc.aspects)
(import [pyherc.aspects [log_debug log_info]])
(import [pyherc.data [Character]])
(import [pyherc.data.effects [EffectHandle]])
(import [functools [partial]])
(import [copy [copy]])

#d(defn generate-creature [configuration model item-generator rng name]
    "Generate creature"
    (let [[config (get configuration name)]
	  [creature (Character model)]
	  [item-adder (partial add-item creature rng item-generator)]
	  [effect-handle-adder (partial add-effect-handle creature)]
	  [effect-adder (partial add-effect creature)]]
      (set-creature-attributes creature config)
      (ap-each (:effect-handles config) (effect-handle-adder it))
      (ap-each (:effects config) (effect-adder it))
      (ap-each (:inventory config) (item-adder it))
      creature))


#d(defn creature-config [name body finesse mind hp speed icons attack 
			 &optional [ai nil] [effect-handles nil] [effects nil]
			 [inventory nil] [description nil]]
    "Create configuration for a creature"
    {:name name :body body :finesse finesse :mind mind :hp hp :speed speed
     :icons icons :attack attack :ai ai :description description
     :effect-handles (if effect-handles effect-handles [])
     :effects (if effects effects [])
     :inventory (if inventory inventory [])})

#d(defn inventory-config [item-name min-amount max-amount probability]
    "Create configuration for inventory item"
    {:item-name item-name :min-amount min-amount :max-amount max-amount
     :probability probability})

(defn set-creature-attributes [creature config]
  (setv creature.name (:name config))
  (setv creature.body (:body config))
  (setv creature.finesse (:finesse config))
  (setv creature.mind (:mind config))
  (setv creature.hit_points (:hp config))
  (setv creature.max_hp (:hp config))
  (setv creature.speed (:speed config))
  (setv creature.icon (:icons config))
  (setv creature.attack (:attack config))
  (when (:ai config)
    (setv creature.artificial-intelligence ((:ai config) creature))))

(defn add-effect [creature effect]
  (.add-effect creature (copy effect)))

(defn add-effect-handle [creature handle-spec]
  (.add-effect-handle creature (EffectHandle handle-spec.trigger
					     handle-spec.effect
					     handle-spec.parameters
					     handle-spec.charges)))

(defn add-item [creature rng item-generator item-spec]
  (let [[item-count (.randint rng (:min-amount item-spec) (:max-amount item-spec))]]
    (for [item (range item-count)]
      (.append creature.inventory
	       (.generate-item item-generator (:item-name item-spec))))))
