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

(import [pyherc.generators.level.decorator [FloorBuilderDecorator
                                            FloorBuilderDecoratorConfig
                                            SurroundingDecorator
                                            SurroundingDecoratorConfig
                                            DirectionalWallDecorator
                                            DirectionalWallDecoratorConfig
                                            floor-swap wall-ornamenter]])

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

(defn animated-pit-builder [base]
  (FloorBuilderDecorator
   (FloorBuilderDecoratorConfig [] 
                                [(+ base "_f0_07") (+ base "_f1_07")]
                                [(+ base "_f0_08") (+ base "_f1_08")]
                                [(+ base "_f0_01") (+ base "_f1_01")]
                                [(+ base "_f0_07") (+ base "_f1_07")]
                                [(+ base "_f0_03") (+ base "_f1_03")]
                                [(+ base "_f0_04") (+ base "_f1_04")]
                                [(+ base "_f0_08") (+ base "_f1_08")]
                                [(+ base "_f0_06") (+ base "_f1_06")]
                                [(+ base "_f0_01") (+ base "_f1_01")]
                                [(+ base "_f0_02") (+ base "_f1_02")]
                                [(+ base "_f0_03") (+ base "_f1_03")]
                                [(+ base "_f0_04") (+ base "_f1_04")]
                                [(+ base "_f0_05") (+ base "_f1_05")]
                                [(+ base "_f0_06") (+ base "_f1_06")]
                                [(+ base "_f0_02") (+ base "_f1_02")]
                                [(+ base "_f0_05") (+ base "_f1_05")]
                                (+ base "_f0_07")
                                [(+ base "_f0_09") (+ base "_f1_09")]
                                [(+ base "_f0_11") (+ base "_f1_11")])))

(defn pit-builder [base]
  (FloorBuilderDecorator
   (FloorBuilderDecoratorConfig [] 
                                (+ base "_07")
                                (+ base "_08") (+ base "_01")
                                (+ base "_07") (+ base "_03")
                                (+ base "_04") (+ base "_08")
                                (+ base "_06") (+ base "_01")
                                (+ base "_02") (+ base "_03")
                                (+ base "_04") (+ base "_05")
                                (+ base "_06") (+ base "_02")
                                (+ base "_05") (+ base "_07")
                                (+ base "_09") (+ base "_11"))))

(defn wall-builder [tile]
  (aggregate-decorator (SurroundingDecorator 
                        (SurroundingDecoratorConfig [] tile))
                       (DirectionalWallDecorator 
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
                                                        tile))))

(defn wall-torches [tile rate rng]
  (wall-ornamenter nil
                   [(+ tile "_37") [["catacombs_torches_f0"
                                     "catacombs_torches_f1"]]]
                   nil
                   rate rng))

;; TODO - move into another file

(defn aggregate-decorator [&rest builders]
  (fn [level]
    (ap-each builders (it level))))
