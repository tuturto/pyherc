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

(require pyherc.macros)

(import [pyherc.generators.level.partitioners [section-to-map section-level]]
        [pyherc.generators.level.room.circle [CircularRoomGenerator]])

(defclass CacheRoomGenerator [CircularRoomGenerator]
  "generator for cache rooms"
  [[--init-- (fn [self floor-tile corridor-tile cache-creator level-types]
               "default constructor"
               (-> (super) (.--init-- floor-tile corridor-tile level-types))
               (setv self.cache-creator cache-creator)
               nil)]
   [generate-room (fn [self section]
                    "generate a new room"
                    (-> (super) (.generate-room section))
                    (self.cache-creator (section-level section)
                                        (section-to-map section self.center-point)))]])
