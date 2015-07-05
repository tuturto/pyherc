;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2015 Tuukka Turto
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

(defn e-event-type [event]
  (:event-type event))

(defn e-level [event]
  (:level event))

(defn e-location [event]
  (:location event))

(defn e-old-level [event]
  (:old-level event))

(defn e-old-location [event]
  (:old-location event))

(defn e-new-level [event]
  (:new-level event))

(defn e-direction [event]
  (:direction event))

(defn e-character [event]
  (:character event))

(defn e-new-character [event]
  (:new-character event))

(defn e-destroyed-characters [event]
  (:destroyed-characters event))

(defn e-attacker [event]
  (:attacker event))

(defn e-type [event]
  (:type event))

(defn e-old-spirit [event]
  (:old-spirit event))

(defn e-new-spirit [event]
  (:new-spirit event))

(defn e-new-hit-points [event]
  (:new-hit-points event))

(defn e-old-hit-points [event]
  (:old-hit-points event))

(defn e-target [event]
  (:target event))

(defn e-healing [event]
  (:healing event))

(defn e-effect [event]
  (:effect event))

(defn e-damage [event]
  (:damage event))

(defn e-damage-type [event]
  (:damage-type event))

(defn e-deceased [event]
  (:deceased event))

(defn e-cache [event]
  (:cache event))

(defn e-item [event]
  (:item event))

(defn e-new-items [event]
  (:new-items event))

(defn e-new-characters [event]
  (:new-characters event))
