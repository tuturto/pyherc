;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2017 Tuukka Turto
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

(defn empty-event []
  {:event-type "empty"
   :level None
   :character None})

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

(defn e-trap [event]
  (:trap event))
