;; -*- coding: utf-8 -*-
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

(defmacro date-rules [&rest rule-specs]
  `(defn get-special-events [year month day]
     (let [[events []]]
       ~@(map (fn [x] `(date-rule ~@x)) rule-specs)
       events)))

(defmacro date-rule [date-name &rest rules]
  (if (> (len rules) 1)
    `(when (and ~@rules) (.append events ~date-name))
    `(when ~@rules (.append events ~date-name))))
