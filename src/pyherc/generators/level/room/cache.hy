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
(require pyherc.macros)

(import [pyherc.data [add-location-feature ornamentation]]
        [pyherc.data.features [new-cache]]
        [pyherc.generators.level.partitioners [section-to-map section-level
                                               section-floor section-data]]
        [pyherc.generators.level.room.circle [CircularRoomGenerator]])

(defn cache-creator [cache-tiles position-selector item-selector
                     character-selector rng]
  "create cache creator"
  (fn [section &optional [trap-generator nil]]
    "fill cache with items and characters"
    (ap-each (position-selector section)
             (add-new-cache cache-tiles
                            (section-level section)
                            (section-to-map section it)
                            character-selector
                            item-selector
                            rng))))

(defn add-new-cache [cache-tiles level location character-selector item-selector
                     rng]
  "add new cache"
  (ornamentation level location (.choice rng cache-tiles))
  (add-location-feature level location
                        (new-cache level
                                   location
                                   (item-selector)
                                   (character-selector))))

(defclass CacheRoomGenerator [CircularRoomGenerator]
  "generator for cache rooms"
  [[--init-- (fn [self floor-tile corridor-tile cache-creator level-types]
               "default constructor"
               (-> (super) (.--init-- floor-tile corridor-tile level-types))
               (setv self.cache-creator cache-creator)
               nil)]
   [generate-room (fn [self section]
                    "generate a new room"
                    (-> (super) (.generate-room section))
                    (self.cache-creator (section-level section)
                                        (section-to-map section
                                                        self.center-point)))]])
