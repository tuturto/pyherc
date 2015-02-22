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
                                            FloorBuilderDecoratorConfig]])

(defmacro floorbuilder [base]
  `(FloorBuilderDecorator 
    (FloorBuilderDecoratorConfig [] ~base
                                 (+ ~base "_1") (+ ~base "_3")
                                 (+ ~base "_5") (+ ~base "_7")
                                 (+ ~base "_13") (+ ~base "_15")
                                 (+ ~base "_17") (+ ~base "_35")
                                 (+ ~base "_37") (+ ~base "_57")
                                 (+ ~base "_135") (+ ~base "_137")
                                 (+ ~base "_157") (+ ~base "_357")
                                 (+ ~base "_1357") ~base
                                 (+ ~base "_1357") (+ ~base "_1357"))))

(setv soil4-floorbuilder (floorbuilder "ground_soil4"))
(setv tile3-floorbuilder (floorbuilder "ground_tile3"))
(setv tile4-floorbuilder (floorbuilder "ground_tile4"))
(setv wood4-floorbuilder (floorbuilder "ground_wood4"))
