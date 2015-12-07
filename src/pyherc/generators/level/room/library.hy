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

(require pyherc.macros)
(require hy.contrib.anaphoric)
(import [pyherc.generators.level.partitioners [section-wall
                                               section-ornamentation
                                               section-to-map]]
        [pyherc.generators.level.room.squareroom [SquareRoomGenerator]]
        random)

(defclass LibraryRoomGenerator [SquareRoomGenerator]
  "generator for library rooms"
  [[--init-- (fn [self floor-tile corridor-tile walls decos rate feature-creator level-types]
               "default constructor"
               (-> (super)
                   (.--init-- floor-tile nil corridor-tile level-types))
               (setv self.walls walls)
               (setv self.decos decos)
               (setv self.rate rate)
               (setv self.feature-creator feature-creator)
               nil)]
   [generate-room (fn [self section]
                    (-> (super)
                        (.generate-room section))                    
                    (ap-each self.rows 
                             (when (<= (.randint random 1 100) self.rate)
                               (when self.walls 
                                 (section-wall section it (.choice random self.walls) "wall"))
                               (when self.decos
                                 (section-ornamentation section it (.choice random self.decos)))
                               (when self.feature-creator
                                 (self.feature-creator (:level section) 
                                                       (section-to-map section it))))))]])
