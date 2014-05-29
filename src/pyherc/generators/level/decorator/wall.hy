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

(import [pyherc.generators.level.decorator.basic [Decorator DecoratorConfig]]
        [pyherc.aspects [log-debug log-info]]
        [pyherc.data [wall-tile floor-tile get-tiles area-around]])
(require pyherc.macros)
(require pyherc.aspects)
(require hy.contrib.anaphoric)

(defclass SurroundingDecorator [Decorator]
  [[--init-- #d(fn [self configuration]
                 "default constructor"
                 (-> (super) (.--init-- configuration))
                 (setv self.wall-tile configuration.wall-tile)
                 nil)]
   [decorate-level #i(fn [self level]
                       "decorate a level"
                       (ap-each (list (get-tiles level))
                                (decorate-tile level it self.wall-tile)))]])

(defn decorate-tile [level loc-tile replacement]
  "decorate single tile"
  (let [[#t(location tile) loc-tile]
        [surrounding-tiles (area-around location)]]
    (ap-each (ap-filter (and (= (wall-tile level it) null)
                             (= (floor-tile level it) null))
                        surrounding-tiles)
             (wall-tile level it replacement))))

(defclass SurroundingDecoratorConfig [DecoratorConfig]
  [[--init-- #d(fn [self level-types wall-tile]
                 "default constructor"
                 (-> (super) (.--init-- level-types))
                 (setv self.wall-tile wall-tile)
                 nil)]])
