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

;; TODO: remove?
(defmacro effect-dsl []
  `(do
     (require [pyherc.macros [*]])))

(defmacro effect [type name attributes &rest body]
  "create a class that defines a new effect"

  (defn helper [&optional trigger add-event remove-event [multiples-allowed 'False]]
    "helper function to construct effect definition"    

    (setv attribute-let [])
    (for [x attributes]
      (.append attribute-let x)
      (.append attribute-let `(. self ~x)))

    (setv add-event-fn (if add-event
                         `(defn get-add-event [self]
                            "get event describing adding this effect"
                            (let ~attribute-let
                              ~add-event))
                         `(defn get-add-event [self]
                            "get event describing adding this effect"
                            (new-effect-added-event self))))

    (setv remove-event-fn (if remove-event
                            `(defn get-removal-event [self]
                               "get event describing removing this effect"
                               (let ~attribute-let
                                 ~remove-event))
                            `(defn get-removal-event [self]
                               "get event describing removing this effect"
                               (new-effect-removed-event self))))
    
    (setv trigger-fn (if trigger
                       `(defn do-trigger [self]
                          (let ~attribute-let
                              ~trigger))
                       `(defn do-trigger [self]
                          None)))

    `(defclass ~type []

       [multiple-allowed ~multiples-allowed
        effect-name ~name]
       
       (defn --init-- [self duration frequency tick icon title
                       description ~@attributes]
         "default initializer"
         (super-init)
         (set-attributes duration frequency tick icon title description)
         (set-attributes ~@attributes))

       (defn trigger [self]
         "trigger the effect"
         (.do-trigger self)
         (.post-trigger self))
       
       ~trigger-fn

       (defn post-trigger [self]
         "do house keeping after effect has been triggered"
         (when (not (none? self.duration))
           (setv self.tick self.frequency)
           (setv self.duration (- self.duration self.frequency))))
       
       ~add-event-fn
       ~remove-event-fn))
  
  (apply helper [] (dict-comp (if (= :trigger (first x)) "trigger" 
                                  (= :add-event (first x)) "add_event"
                                  (= :remove-event (first x)) "remove_event"
                                  (= :multiple-allowed (first x)) "multiples_allowed"
                                  x)
                              (second x)
                              [x (partition body)])))
