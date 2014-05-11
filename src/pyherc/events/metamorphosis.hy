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

(defclass MetamorphosisEvent [Event]
  "event to indicate that a metamorphosis has occurred"
  [[--init-- #d(fn [self character new-character &optional destroyed-characters]
		 "default constructor"
		 (-> (super) (.--init-- "metamorphosis"
					character.level
					character.location
					[]))
		 (setv self.character character)
		 (setv self.new-character new-character)
                 (setv self.destroyed-characters destroyed-characters)
		 nil)]
   [get-description (fn [self point-of-view]
		      "get description of this event"
		      (if (= point-of-view self.character)
			(-> "You have morphed to {0}" (.format self.new-character))
			(-> "{0} has morphed to {1}" (.format self.character
                                                              self.new-character))))]])
