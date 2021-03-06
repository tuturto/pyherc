;; -*- coding: utf-8 -*-
;;
;; Copyright (c) 2010-2017 Tuukka Turto
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

(require [hy.extra.anaphoric [*]])

(import [herculeum.ui.gui.animations.animation [Animation]]
        [herculeum.ui.gui [layers]]
        [pyherc.events [e-character e-new-items e-new-characters]])

(defclass DigAnimation [Animation]
  "animation for digging"
  (defn --init-- [self event]
    (-> (super) (.--init-- event))
    (setv self.character (e-character event))
    (setv self.items (e-new-items event))
    (setv self.characters (e-new-characters event)))
  
  (defn trigger [self ui]
    (ap-each self.items (.add-glyph ui it ui.scene
                                    layers.zorder-item))
    (ap-each self.characters (.add-glyph ui it ui.scene
                                         layers.zorder-character))))
