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

(import [pyherc.generators.level.partitioners [section-floor
                                               section-wall
                                               section-ornamentation]])

(defn floor-creator [floor-tiles position-selector rng]
  "create floor creator"
  (fn [section &optional [trap-generator nil]]
    "fill given area randomly with floor"
    (ap-each (position-selector section)
             (section-floor section it (.choice rng floor-tiles) nil))))

(defn wall-creator [wall-tiles position-selector rng]
  "create wall creator"
  (fn [section &optional [trap-generator nil]]
    "fill given area randomly with walls"
    (ap-each (position-selector section)
             (section-wall section it (.choice rng wall-tiles) nil))))

(defn ornament-creator [ornament-tiles position-selector rate rng]
  "create ornament creator"
  (fn [section &optional [trap-generator nil]]
    "fill given area randomly with ornaments"
    (ap-each (position-selector section)       
             (when (<= (.randint rng 0 100) rate) 
               (section-ornamentation section it 
                                      (.choice rng ornament-tiles))))))
