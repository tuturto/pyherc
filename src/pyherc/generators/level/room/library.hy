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
(require hy.contrib.anaphoric)
(import [pyherc.generators.level.room.squareroom [SquareRoomGenerator]]
        random)

(defclass LibraryRoomGenerator [SquareRoomGenerator]
  "generator for library rooms"
  [[--init-- (fn [self floor-tile corridor-tile walls decos rate level-types]
               "default constructor"
               (-> (super)
                   (.--init-- floor-tile nil corridor-tile level-types))
               (setv self.walls walls)
               (setv self.decos decos)
               (setv self.rate rate)
               nil)]
   [generate-room (fn [self section]
                    (-> (super)
                        (.generate-room section))                    
                    (ap-each self.rows 
                             (when (<= (.randint random 1 100) self.rate)
                               (when self.walls 
                                 (.set-wall section it (.choice random self.walls) "wall"))
                               (when self.decos
                                 (.set-ornamentation section it (.choice random self.decos))))))]])
