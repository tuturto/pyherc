;; -*- coding: utf-8 -*-
;;
;;  Copyright 2010-2014 Tuukka Turto
;;
;;  This file is part of pyherc.
;;
;;  pyherc is free software: you can redistribute it and/or modify
;;  it under the terms of the GNU General Public License as published by
;;  the Free Software Foundation, either version 3 of the License, or
;;  (at your option) any later version.
;;
;;  pyherc is distributed in the hope that it will be useful,
;;  but WITHOUT ANY WARRANTY; without even the implied warranty of
;;  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;;  GNU General Public License for more details.
;;
;;  You should have received a copy of the GNU General Public License
;;  along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

(require pyherc.aspects)
(import [pyherc.rules.public [ActionParameters]]
	[pyherc.aspects [log-debug log-info]])

#d(defn exhume [character action-factory]
    "perform exhuming"
    (let [[action (.get-action action-factory (ExhumeParameters character))]]
      (when (.legal? action)
        (.execute action))))

(defn mexhume-legal? [character action-factory]
  "check if exhuming is legal"
  (let [[action (.get-action action-factory
                             (ExhumeParameters character))]]
    (.legal? action)))

(defclass ExhumeParameters [ActionParameters]
  "Class controlling creation of ExhumeAction"
  [[--init-- #d(fn [self character]
		 (-> (super) (.--init--))
		 (setv self.action-type "exhume")
		 (setv self.character character)
		 nil)]])