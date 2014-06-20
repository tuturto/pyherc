;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2014 Tuukka Turto
;;
;;   This file is part of pyherc.
;;
;;   pyherc is free software: you can redistribute it and/or modify
;;   it under the terms of the GNU General Public License as published by
;;   the Free Software Foundation, either version 3 of the License, or
;;   (at your option) any later version.
;;
;;   pyherc is distributed in the hope that it will be useful,
;;   but WITHOUT ANY WARRANTY; without even the implied warranty of
;;   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;   GNU General Public License for more details.
;;
;;   You should have received a copy of the GNU General Public License
;;   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

(require hy.contrib.anaphoric)
(require pyherc.macros)

(import [pyherc.data [add-location-tag add-trap floor-tile wall-tile
                      ornamentation distance-between get-location-tags]])

(defn new-section [corner0 corner1 level random-generator]
  "create a new section"
  {:corners [corner0 corner1]
   :level level
   :connections []
   :room-connections []
   :neighbours []
   :data {}
   :random-generator random-generator})

(defn section-data [section key &optional [value :no-data]]
  "get/set section custom data"
  (when (!= value :no-data)
    (assoc (:data section) key value))
  (get (:data section) key))

(defn section-corners [section &optional [corners :no-corners]]
  "get/set corners of this section"
  (when (!= corners :no-corners) (setv (:corners section) corners))
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
  (let [[point₀ (x-coordinate (first (:corners section)))]
        [point₁ (x-coordinate (second (:corners section)))]]
    (min point₀ point₁)))

(defn right-edge [section]
  "get right edge of the section"
  (let [[point₀ (x-coordinate (first (:corners section)))]
        [point₁ (x-coordinate (second (:corners section)))]]
    (max point₀ point₁)))

(defn top-edge [section]
  "get top edge of the section"
  (let [[point₀ (y-coordinate (first (:corners section)))]
        [point₁ (y-coordinate (second (:corners section)))]]
    (min point₀ point₁)))

(defn bottom-edge [section]
  "get bottom edge of the section"
  (let [[point₀ (y-coordinate (first (:corners section)))]
        [point₁ (y-coordinate (second (:corners section)))]]
    (max point₀ point₁)))

(defn section-to-map [section location]
  "map section coordinates to map coordinates"
  #t((+ (left-edge section) (x-coordinate location))
     (+ (top-edge section) (y-coordinate location))))

(defn section-floor [section location &optional [tile-id :no-tile] location-type]
  "get/set floor tile in section"
  (let [[loc (section-to-map section location)]
        [level (:level section)]]
    (when (!= tile-id :no-tile) (floor-tile level loc tile-id))
    (when location-type (add-location-tag level loc location-type))
    (floor-tile level loc tile-id)))

(defn section-wall [section location &optional [tile-id :no-tile] location-type]
  "get/set wall tile in section"
  (let [[loc (section-to-map section location)]
        [level (:level section)]]
    (when (!= tile-id :no-tile) (wall-tile level loc tile-id))
    (when location-type (add-location-tag level loc location-type))
    (wall-tile level loc tile-id)))

(defn section-ornamentation [section location &optional [tile-id :no-tile]]
  "get/set ornament in section"
  (let [[loc (section-to-map section location)]
        [level (:level section)]]
    (when (!= tile-id :no-tile) (ornamentation level loc tile-id))
    (ornamentation level loc tile-id)))

(defn section-trap [section location trap]
  "set trap in section"
  (add-trap (:level section) (section-to-map section location) trap))

(defn section-location-tag [section location &optional [location-tag :no-tag]]
  "get/set location type in section"
  (let [[loc (section-to-map section location)]
        [level (:level section)]]
    (when (!= location-tag :no-tag) (add-location-tag level loc location-tag))
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
  (.append (:room-connections section) (Connection nil
                                                   location 
                                                   direction 
                                                   section)))

(defn neighbour-sections [section]
  "get sections next to this one"
  (genexpr sec [sec (:neighbours section)]))

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
  (let [[#t(corner₀ corner₁) (section-corners section)]]
    (for [loc (range (+ (x-coordinate corner₀) 1) (x-coordinate corner₁))]
      (do (yield #t(loc (y-coordinate corner₀) "down"))
          (yield #t(loc (y-coordinate corner₁) "up"))))
    (for [loc (range (+ (y-coordinate corner₀) 1) (y-coordinate corner₁))]
      (do (yield #t((x-coordinate corner₀) loc "right"))
          (yield #t((x-coordinate corner₁) loc "left"))))))

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
  (let [[direction section-connection.direction]
        [wanted (cond [(= direction "right") "left"]
                      [(= direction "left") "right"]
                      [(= direction "up") "down"]
                      [(= direction "down") "up"])]
        [possible (list-comp x [x (:room-connections section)]
                             (= x.direction wanted))]]
    (.choice (:random-generator section) possible)))

(defn connect-sections [section neighbour]
  "connect two sections"
  (let [[my-side-of-border (list (common-border section neighbour))]
        [my-side (.choice (:random-generator section) my-side-of-border)]
        [my-connection (Connection neighbour 
                                   #t((x-coordinate my-side)
                                      (y-coordinate my-side))
                                   (get my-side 2)
                                   section)]
        [other-side (opposing-point neighbour my-side)]
        [other-connection (Connection section
                                      #t((x-coordinate other-side)
                                         (y-coordinate other-side))
                                      (get other-side 2)
                                      neighbour)]]

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
  [[--init-- (fn [self connection location direction section]
               "default constructor"
               (-> (super) (.--init--))
               (setv self.connection connection)
               (setv self.location location)
               (setv self.direction direction)
               (setv self.section section)
               nil)]
   [translate-to-section (fn [self]
                           "create a new connection with coordinates translated to section"
                           (Connection self.connection
                                       #t((- (x-coordinate self.location)
                                             (left-edge self.section))
                                          (- (y-coordinate self.location)
                                             (top-edge self.section)))
                                       self.direction
                                       self.section))]])
