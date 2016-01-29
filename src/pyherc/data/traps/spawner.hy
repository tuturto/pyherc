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

(import [random]
        [pyherc.data.traps.trap [Trap]]
        [pyherc.data [blocks-movement add-character]]
        [pyherc.data.geometry [area-around]])

(defclass CharacterSpawner [Trap]
  [[--init-- (fn [self character-selector &optional [icon nil]]
               (super-init icon)
               (set-attributes character-selector)
               nil)]
   [on-trigger (fn [self]
                 (let [[creatures (self.character-selector)]
                       [area (area-around self.location)]]
                   (ap-each creatures (place-creature it self.level area))))]])

(defn place-creature [creature level area]
  (let [[free-spots (list (ap-filter (not (blocks-movement level it))
                                     area))]]
    (when free-spots
      (add-character level
                     (.choice random free-spots)
                     creature))))
