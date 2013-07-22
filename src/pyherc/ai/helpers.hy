;; -*- coding: utf-8 -*-
;;
;;   Copyright 2010-2013 Tuukka Turto
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

(setv __doc__ "helper macros and functions for AIs")

(def direction-mapping {1 :north 2 :north-east 3 :east 4 :south-east 5 :south
			6 :south-west 7 :west 8 :north-west 9 :enter
			:north 1 :north-east 2 :east 3 :south-east 4 :south 5
			:south-west 6 :west 7 :north-west 8 :enter 9})

(defn map-direction [direction]
  "map between keyword and integer directions"
  (get direction-mapping direction))

(defmacro second [collection]
  (quasiquote (get (unquote collection) 1)))

(defmacro third [collection]
  (quasiquote (get (unquote collection) 2)))

(defmacro fourth [collection]
  (quasiquote (get (unquote collection) 3)))
