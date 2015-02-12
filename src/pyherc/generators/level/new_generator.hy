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

(import [pyherc.data [new-level Portal add-portal get-locations-by-tag
                      wall-tile]]
        [pyherc.generators.level.partitioners.old-grid [RandomConnector]])

(defn new-level-generator [model partitioners room-generators decorators
                           portal-adders item-adders creature-adders
                           rng level-context]
  "create a new level generator function"
  (fn [portal]
    (let [[level (new-level model)]
          [partitioner (.choice rng partitioners)]
          [connector (RandomConnector rng)]
          [sections (.connect-sections connector (partitioner level))]]
      (ap-each sections ((.choice rng room-generators) it))
      (ap-each portal-adders (.add-portal it level))
      (when portal (let [[rooms (list (get-locations-by-tag level "room"))]]
                     (when rooms (add-portal level
                                             (.choice rng rooms)
                                             (Portal #t(portal.other-end-icon nil) nil)
                                             portal))))
      (ap-each creature-adders (.add-creatures it level))
      (ap-each item-adders (.add-items it level))
      (ap-each decorators (.decorate-level it level))
      level)))
