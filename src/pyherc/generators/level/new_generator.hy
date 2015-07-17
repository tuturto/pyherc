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

(import [pyherc.data [new-level Portal add-portal get-locations-by-tag
                      wall-tile level-name level-description]]
        [pyherc.generators.level.partitioners.old-grid [RandomConnector]])

(defmacro run-generators-for [level &rest generators]
  `(do ~@(map (fn [x] `(ap-each ~x (it ~level))) generators)))

(defn new-level-generator [model partitioners room-generators decorators
                           portal-adders item-adders creature-adders
                           rng name description]
  "create a new level generator function"
  (fn [portal]
    (let [[level (new-level model)]
          [partitioner (.choice rng partitioners)]
          [connector (RandomConnector rng)]
          [sections (.connect-sections connector (partitioner level))]]
      (level-name level name)
      (level-description level description)
      (ap-each sections ((.choice rng room-generators) it))
      (when creature-adders ((.choice rng creature-adders) level))
      (when item-adders ((.choice rng item-adders) level))
      (run-generators-for level
                          portal-adders
                          decorators)
      (when portal
        (let [[rooms (genexpr x [x (get-locations-by-tag level "room")]
                              (suitable-location level x))]]
          (when rooms (add-portal level
                                  (.choice rng rooms)
                                  (Portal #t(portal.other-end-icon nil) nil)
                                  portal))))
      level)))
