;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2015 Tuukka Turto
;;
;;  This file is part of pyherc.
;;
;;  pyherc is free software: you can redistribute it and/or modify
;;  it under the terms of the GNU General Public License as published by
;;  the Free Software Foundation either version 3 of the License or
;;  (at your option) any later version.
;;
;;  pyherc is distributed in the hope that it will be useful
;;  but WITHOUT ANY WARRANTY; without even the implied warranty of
;;  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;  GNU General Public License for more details.
;;
;;  You should have received a copy of the GNU General Public License
;;  along with pyherc.  If not see <http://www.gnu.org/licenses/>.


(defn item-by-type [min-amount max-amount item-type &optional [location nil]]
  "configuration for including item by name"
  (if location {"min_amount" min-amount "max_amount" max-amount "name" nil
                "type" item-type "location" location}
      {"min_amount" min-amount "max_amount" max-amount "name" nil
       "type" item-type "location" "room"}))

(defn item-by-name [min-amount max-amount name &optional [location nil]]
  "configuration for including item by type"
  (if location {"min_amount" min-amount "max_amount" max-amount "name" name
                "type" nil "location" location}
      {"min_amount" min-amount "max_amount" max-amount "name" name
       "type" nil "location" "room"}))
