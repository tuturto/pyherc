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

(require [hy.extra.anaphoric [ap-each ap-filter]])
(require [pyherc.aspects [*]])
(require [pyherc.macros [*]])
(import [hymn.types.either [Left Right]]
        [pyherc.aspects [log-debug]]
        [pyherc.data [skill-ready? cooldown blocks-movement get-character
                      get-characters add-character]]
        [pyherc.data.level [traps↜]]
        [pyherc.data.geometry [area-around]]
        [pyherc.data.constants [Duration]]
        [pyherc.events.mitosis [new-mitosis-event]]
        [pyherc])

(defclass MitosisAction []
  [--init-- (fn [self character character-generator rng character-limit]
              "default constructor"
              (-> (super) (.--init--))
              (setv self.character character)
              (setv self.character-generator character-generator)
              (setv self.rng rng)
              (setv self.character-limit character-limit))
   legal? (fn [self]
            "check if action is possible to perform"
            (let [location self.character.location
                  level self.character.level]
              (if (and
                   (skill-ready? self.character "mitosis")
                   (list (free-tiles level (area-around location)))
                   (< (count (ap-filter (= self.character.name it.name) (get-characters level)))
                      self.character-limit))
                True False)))
   execute (fn [self]
             "execute the action"
             (if (.legal? self)
               (let [new-character (self.character-generator self.character.name)
                     location self.character.location
                     level self.character.level
                     tiles (list (free-tiles level (area-around location)))]
                 (add-character level (.choice self.rng tiles) new-character)
                 (.add-to-tick self.character Duration.very-slow)
                 (.add-to-tick new-character Duration.very-slow)
                 (cooldown self.character "mitosis" (* 6 Duration.very-slow))
                 (cooldown new-character "mitosis" (* 6 Duration.very-slow))
                 (.raise-event self.character (new-mitosis-event self.character
                                                                 new-character))
                 (ap-each (traps↜ new-character.level new-character.location)
                          (.on-enter it new-character))
                 (call check-dying new-character)
                 (Right self.character))
               (Left self.character)))])

#d(defn free-tiles [level tiles]
    (ap-filter (not (or
                     (blocks-movement level it)
                     (get-character level it)))
               tiles))
