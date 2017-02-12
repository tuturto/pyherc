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

(defn new-dungeon []
  "create new instance of dungeon config"
  {})

(defn add-level [dungeon level]
  "add new level config into dungeon config"
  (assoc dungeon (:level-name level) level))

(defmacro merge-component-list [component-name dungeon level]
  `(.extend (get (get ~dungeon (:level-name level)) ~component-name)
            (get ~level ~component-name)))

(defmacro level-config [component-name dungeon level-name]
  `(list-comp x [x (~component-name (get ~dungeon ~level-name))]))

(defn merge-level [dungeon level]
  "merge new level config into existing dungeon data"
  (when (not (in (:level-name level) dungeon))    
    (add-level dungeon (new-level (:level-name level)
                                  [] [] [] [] [] [] (:description level))))
  (ap-each (genexpr comp [comp (.keys level)] (not (in comp [:level-name :description])))
           (merge-component-list it dungeon level)))

(defn new-level [level-name room-generators partitioners decorators
                 items characters portal-config description]
  "create new instance of level config"
  {:level-name level-name
   :description description
   :room-generators room-generators
   :partitioners partitioners
   :decorators decorators
   :items items
   :characters characters
   :portal-config portal-config})

(defn room-generators [dungeon level-name]
  "get room generators for given level"
  (level-config :room-generators dungeon level-name))

(defn level-partitioners [dungeon level-name]
  "get level partitioners for given level"
  (level-config :partitioners dungeon level-name))

(defn decorators [dungeon level-name]
  "get level decorators for given level"
  (level-config :decorators dungeon level-name))

(defn items [dungeon level-name]
  "get items for given level"
  (level-config :items dungeon level-name))

(defn characters [dungeon level-name]
  "get characters for given level"
  (level-config :characters dungeon level-name))

(defn portals [dungeon level-name]
  "get portal configs"
  (level-config :portal-config dungeon level-name))

(defn description [dungeon level-name]
  "get level description"
  (:description (get dungeon level-name)))
