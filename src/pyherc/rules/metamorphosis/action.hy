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

(require [hy.extra.anaphoric [ap-each]])
(require [pyherc.aspects [*]])
(require [pyherc.macros [*]])
(import [hymn.types.either [Left Right]]
        [pyherc.aspects [log-debug]]
        [pyherc.data [skill-ready? cooldown add-character remove-character]]
        [pyherc.data.constants [Duration]]
        [pyherc.events.metamorphosis [new-metamorphosis-event]])

(defclass MetamorphosisAction []
  
  []

  (defn --init-- [self character new-character-name character-generator rng
                  destroyed-characters]
    "default constructor"
    (super-init)
    (set-attributes character new-character-name character-generator
                    rng)
    (setv self.destroyed-characters (list destroyed-characters)))
  
  (defn legal? [self]
    "check if action is possible to perform"
    (skill-ready? self.character "metamorphosis"))
  
  (defn execute [self]
    "execute the action"
    (if (.legal? self)
      (let [new-character (self.character-generator self.new-character-name)
            location self.character.location
            level self.character.level]
        (remove-character level self.character)
        (add-character level location new-character)
        (.add-to-tick new-character Duration.slow)
        (cooldown new-character "metamorphosis" (* 2 Duration.very-slow))
        (ap-each self.destroyed-characters
                 (remove-character level it))
        (.raise-event self.character (new-metamorphosis-event self.character
                                                              new-character
                                                              self.destroyed-characters))
        (Right self.character))
      (Left self.character))))
