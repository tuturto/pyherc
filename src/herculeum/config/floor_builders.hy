;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2015 Tuukka Turto
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

(require hy.contrib.anaphoric)

(import [pyherc.generators.level.decorator [FloorBuilderDecorator
                                            FloorBuilderDecoratorConfig
                                            SurroundingDecorator
                                            SurroundingDecoratorConfig
                                            DirectionalWallDecorator
                                            DirectionalWallDecoratorConfig
                                            wall-ornamenter]])

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
  )

;; TODO - move into another file

(defn aggregate-decorator [&rest builders]
  (fn [level]
    (ap-each builders (it level))))
