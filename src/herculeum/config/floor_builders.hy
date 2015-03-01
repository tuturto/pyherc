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

(import [pyherc.generators.level.decorator [FloorBuilderDecorator
                                            FloorBuilderDecoratorConfig
                                            SurroundingDecorator
                                            SurroundingDecoratorConfig
                                            DirectionalWallDecorator
                                            DirectionalWallDecoratorConfig]])

(defn floor-builder [base]
  (FloorBuilderDecorator 
   (FloorBuilderDecoratorConfig [] base
                                (+ base "_1") (+ base "_3")
                                (+ base "_5") (+ base "_7")
                                (+ base "_13") (+ base "_15")
                                (+ base "_17") (+ base "_35")
                                (+ base "_37") (+ base "_57")
                                (+ base "_135") (+ base "_137")
                                (+ base "_157") (+ base "_357")
                                (+ base "_1357") base
                                (+ base "_1357") (+ base "_1357"))))

(defn wall-builder [tile]
  (fn [level]
    (let [[decor1 (SurroundingDecorator (SurroundingDecoratorConfig [] tile))]
          [decor2 (DirectionalWallDecorator 
                   (DirectionalWallDecoratorConfig []
                                                   (+ tile "_37")
                                                   (+ tile "_13")
                                                   (+ tile "_35")
                                                   (+ tile "_17")
                                                   (+ tile "_57")
                                                   (+ tile "_15")
                                                   (+ tile "_137")
                                                   (+ tile "_357")
                                                   (+ tile "_135")
                                                   (+ tile "_157")
                                                   (+ tile "_1357")
                                                   tile))]]
      (decor1 level)
      (decor2 level))))

(setv soil1-floorbuilder (floor-builder "ground_soil1"))
(setv soil2-floorbuilder (floor-builder "ground_soil2"))
(setv soil3-floorbuilder (floor-builder "ground_soil3"))
(setv soil4-floorbuilder (floor-builder "ground_soil4"))
(setv tile3-floorbuilder (floor-builder "ground_tile3"))
(setv tile4-floorbuilder (floor-builder "ground_tile4"))
(setv wood4-floorbuilder (floor-builder "ground_wood4"))
