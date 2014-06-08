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

(require pyherc.aspects)
(import [pyherc.aspects [log-debug]]
	[pyherc.events.event [Event]])

(defclass ExhumeEvent [Event]
  "event to indicate that a somebody looted a grave"
  [[--init-- #d(fn [self character grave new-items new-characters]
		 "default constructor"
		 (-> (super) (.--init-- "exhume"
					character.level
					character.location
					[]))
		 (setv self.character character)
                 (setv self.grave grave)
                 (setv self.new-items new-items)
                 (setv self.new-characters new-characters)
		 nil)]
   [get-description (fn [self point-of-view]
		      "get description of this event"
                      (cond [(monster? self)
                             (if (= point-of-view self.character)
                               "The grave was occupied by a monster!"
                               (-> "{0} has unearthed a monster!" (.format self.character)))]
                            [(only-items? self)
                             (if (= point-of-view self.character)
                               "There were something in grave"
                               (-> "{0} has unearthed something" (.format self.character)))]
                            [(empty-grave? self)
                               (if (= point-of-view self.character)
                                 "The grave is empty.."
                                 (-> "{0} has tried to loot an empty grave" (.format self.character)))]))]])

(defn monster? [event]
  "check if the grave contained a monster"
  event.new-characters)

(defn only-items? [event]
  "check if only items were present"
  (and event.new-items (not event.new-characters)))

(defn empty-grave? [event]
  "check if the grave was completely empty"
  (and (not event.new-items) (not event.new-characters)))
