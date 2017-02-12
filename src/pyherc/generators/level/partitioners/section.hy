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

(require [hy.extra.anaphoric [ap-map ap-filter ap-first]])
(require [pyherc.macros [*]])

(import [pyherc.data [add-location-tag add-trap floor-tile wall-tile
                      ornamentation distance-between get-location-tags]])

(defclass Section [dict]
  [--repr-- (fn [self] (str (:corners self)))])

(defn new-section [corner0 corner1 level random-generator]
  "create a new section"
  (let [temp (Section)]
    (assoc temp :corners [corner0 corner1])
    (assoc temp :border None)
    (assoc temp :level level)
    (assoc temp :connections [])
    (assoc temp :room-connections [])
    (assoc temp :neighbours [])
    (assoc temp :data {})
    (assoc temp :random-generator random-generator)
    temp))

(defn equal-sections? [section1 section2]
  "two sections are considered equal when they occupy the same area"
  (= (section-corners section1) (section-corners section2)))

(defn section-in? [section sections]
  "check if given section is in a list of sections"
  (any (ap-map (equal-sections? section it) sections)))

(defn section-data [section key &optional [value "no-data"]]
  "get/set section custom data"
  (when (!= value "no-data")
    (assoc (:data section) key value))
  (get (:data section) key))

(defn section-corners [section &optional [corners "no-corners"]]
  "get/set corners of this section"
  (when (!= corners "no-corners") (setv (:corners section) corners))
  (:corners section))

(defn section-level [section]
  "get level where section is placed"
  (:level section))

(defn section-height [section]
  "get height of a section"
  (abs (- (y-coordinate (first (:corners section)))
          (y-coordinate (second (:corners section))))))

(defn section-width [section]
  "get width of a section"
  (abs (- (x-coordinate (first (:corners section)))
          (x-coordinate (second (:corners section))))))

(defn left-edge [section]
  "get left edge of the section"
  (let [point₀ (x-coordinate (first (:corners section)))
        point₁ (x-coordinate (second (:corners section)))]
    (min point₀ point₁)))

(defn right-edge [section]
  "get right edge of the section"
  (let [point₀ (x-coordinate (first (:corners section)))
        point₁ (x-coordinate (second (:corners section)))]
    (max point₀ point₁)))

(defn top-edge [section]
  "get top edge of the section"
  (let [point₀ (y-coordinate (first (:corners section)))
        point₁ (y-coordinate (second (:corners section)))]
    (min point₀ point₁)))

(defn bottom-edge [section]
  "get bottom edge of the section"
  (let [point₀ (y-coordinate (first (:corners section)))
        point₁ (y-coordinate (second (:corners section)))]
    (max point₀ point₁)))

(defn section-to-map [section location]
  "map section coordinates to map coordinates"
  #t((+ (left-edge section) (x-coordinate location))
     (+ (top-edge section) (y-coordinate location))))

(defn section-floor [section location &optional [tile-id "no-tile"] location-type]
  "get/set floor tile in section"
  (let [loc (section-to-map section location)
        level (:level section)]
    (when (!= tile-id "no-tile") (floor-tile level loc tile-id))
    (when location-type (add-location-tag level loc location-type))
    (floor-tile level loc tile-id)))

(defn section-wall [section location &optional [tile-id "no-tile"] location-type]
  "get/set wall tile in section"
  (let [loc (section-to-map section location)
        level (:level section)]
    (when (!= tile-id "no-tile") (wall-tile level loc tile-id))
    (when location-type (add-location-tag level loc location-type))
    (wall-tile level loc tile-id)))

(defn section-ornamentation [section location &optional [tile-id "no-tile"]]
  "get/set ornament in section"
  (let [loc (section-to-map section location)
        level (:level section)]
    (when (!= tile-id "no-tile") (ornamentation level loc tile-id))
    (ornamentation level loc tile-id)))

(defn section-trap [section location trap]
  "set trap in section"
  (add-trap (:level section) (section-to-map section location) trap))

(defn section-location-tag [section location &optional [location-tag "no-tag"]]
  "get/set location type in section"
  (let [loc (section-to-map section location)
        level (:level section)]
    (when (!= location-tag "no-tag") (add-location-tag level loc location-tag))
    (get-location-tags level loc)))

(defn section-connections [section]
  "get connections of a section"
  (genexpr con [con (:connections section)]))

(defn add-section-connection [section connection]
  "add a new connection to a section"
  (.append (:connections section) connection))

(defn room-connections [section]
  "get room connections of a section"
  (genexpr con [con (:room-connections section)]))

(defn connected? [section]
  "is this section connected"
  (count (section-connections section)))

(defn add-room-connection [section location direction]
  "add a new room connection to a section"
  (.append (:room-connections section) (Connection None
                                                   location 
                                                   direction 
                                                   section)))

(defn neighbour-sections [section]
  "get sections next to this one"
  (genexpr sec [sec (:neighbours section)]))

(defn mark-all-neighbours [sections]
  "process list of sections and mark all neighbours"
  (for [#t(id₀ section₀) (enumerate sections)]
    (for [#t(id₁ section₁) (enumerate sections)]
      (when (and (> id₁ id₀)
                 (adjacent-sections? section₀ section₁))
        (mark-neighbours section₀ section₁)))))

(defn adjacent-sections? [section another-section]
  "check if two sections are adjacent to each other
   very corners are not considered"
  (let [#t(corner₀₀ corner₀₁) (section-corners section)
        #t(corner₁₀ corner₁₁) (section-corners another-section)]
    (or (and (or (= (abs (- (x-coordinate corner₁₁)
                            (x-coordinate corner₀₀))) 1)
                 (= (abs (- (x-coordinate corner₁₀)
                            (x-coordinate corner₀₁))) 1))
             (or (<= (y-coordinate corner₀₀)
                     (y-coordinate corner₁₀)
                     (y-coordinate corner₀₁))
                 (<= (y-coordinate corner₀₀)
                     (y-coordinate corner₁₁)
                     (y-coordinate corner₀₁)))
             (> (len (list (common-border section another-section))) 0))
        (and (or (= (abs (- (y-coordinate corner₁₀)
                            (y-coordinate corner₀₁))) 1)
                 (= (abs (- (y-coordinate corner₀₀)
                            (y-coordinate corner₁₁))) 1))
             (or (<= (x-coordinate corner₀₀)
                     (x-coordinate corner₁₀)
                     (x-coordinate corner₀₁))
                 (<= (x-coordinate corner₀₀)
                     (x-coordinate corner₁₁)
                     (x-coordinate corner₀₁)))
             (> (len (list (common-border section another-section))) 0)))))

(defn mark-neighbours [section neighbour]
  "mark two sections as neighbours"
  (.append (:neighbours section) neighbour)
  (.append (:neighbours neighbour) section))

(defn unconnected-neighbours [section]
  "get unconnected neighbours of a section"
  (ap-filter (not (connected? it)) (neighbour-sections section)))

(defn unconnected-neighbours? [section]
  "check if this section has unconnected neighbours"
  (count (unconnected-neighbours section)))

(defn section-border [section]
  "get border locations of a section"
  (when (not (:border section))
    (let [#t(corner₀ corner₁) (section-corners section)
          temp-border []]
      (for [loc (range (+ (x-coordinate corner₀) 1) (x-coordinate corner₁))]
        (do (.append temp-border #t(loc (y-coordinate corner₀) "down"))
            (.append temp-border #t(loc (y-coordinate corner₁) "up"))))
      (for [loc (range (+ (y-coordinate corner₀) 1) (y-coordinate corner₁))]
        (do (.append temp-border #t((x-coordinate corner₀) loc "right"))
            (.append temp-border #t((x-coordinate corner₁) loc "left"))))
      (assoc section :border temp-border)))
  (:border section))

(defn common-border [section neighbour]
  "get common border between two sections"
  (for [point₀ (section-border section)]
    (for [point₁ (section-border neighbour)]
      (when (= (distance-between point₀ point₁) 1)
        (yield point₀)))))

(defn opposing-point [section location]
  "get point on border that is next to given location"
  (ap-first (= (distance-between it location) 1) (section-border section)))

(defn match-section-to-room [section section-connection]
  "find room connection that matches given section connection"
  (let [direction section-connection.direction
        wanted (if (= direction "right") "left"
                   (= direction "left") "right"
                   (= direction "up") "down"
                   (= direction "down") "up")
        possible (list-comp x [x (:room-connections section)]
                            (= x.direction wanted))]
    (.choice (:random-generator section) possible)))

(defn connect-sections [section neighbour]
  "connect two sections"
  (let [my-side-of-border (list (common-border section neighbour))
        my-side (.choice (:random-generator section) my-side-of-border)
        my-connection (Connection neighbour 
                                  #t((x-coordinate my-side)
                                     (y-coordinate my-side))
                                  (get my-side 2)
                                  section)
        other-side (opposing-point neighbour my-side)
        other-connection (Connection section
                                     #t((x-coordinate other-side)
                                        (y-coordinate other-side))
                                     (get other-side 2)
                                     neighbour)]

    (add-section-connection section my-connection)
    (add-section-connection neighbour other-connection)))

(defn connected-left [section]
  (list-comp x [x (section-connections section)]
             (= x.direction "right")))

(defn connected-right [section]
  (list-comp x [x (section-connections section)]
             (= x.direction "left")))

(defn connected-up [section]
  (list-comp x [x (section-connections section)]
             (= x.direction "down")))

(defn connected-down [section]
  (list-comp x [x (section-connections section)]
             (= x.direction "up")))


(defclass Connection []
  "connection between sections or section and room"
  [--init-- (fn [self connection location direction section]
              "default constructor"
              (-> (super) (.--init--))
              (setv self.connection connection)
              (setv self.location location)
              (setv self.direction direction)
              (setv self.section section))
   translate-to-section (fn [self]
                          "create a new connection with coordinates translated to section"
                          (Connection self.connection
                                      #t((- (x-coordinate self.location)
                                            (left-edge self.section))
                                         (- (y-coordinate self.location)
                                            (top-edge self.section)))
                                      self.direction
                                      self.section))])
