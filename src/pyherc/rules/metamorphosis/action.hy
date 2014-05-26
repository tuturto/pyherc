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
(require pyherc.aspects)
(require pyherc.macros)
(import [pyherc.aspects [log-debug]]
        [pyherc.data [skill-ready? cooldown add-character remove-character]]
        [pyherc.data.constants [Duration]]
	[pyherc.events.metamorphosis [MetamorphosisEvent]])

(defclass MetamorphosisAction []
  [[--init-- #d(fn [self character new-character-name character-generator rng
                    destroyed-characters]
		 "default constructor"
		 (-> (super) (.--init--))
		 (setv self.character character)
                 (setv self.new-character-name new-character-name)
		 (setv self.character-generator character-generator)
		 (setv self.rng rng)
                 (setv self.destroyed-characters (list destroyed-characters))
		 nil)]
   [legal? #d(fn [self]
	       "check if action is possible to perform"
               (skill-ready? self.character :metamorphosis))]
   [execute #d(fn [self]
		"execute the action"
                (let [[new-character (self.character-generator self.new-character-name)]
                      [location self.character.location]
                      [level self.character.level]]
                  (remove-character level self.character)
                  (add-character level location new-character)
                  (.add-to-tick new-character Duration.slow)
                  (cooldown new-character :metamorphosis (* 2 Duration.very-slow))
                  (ap-each self.destroyed-characters
                           (remove-character level it))
                  (.raise-event self.character (MetamorphosisEvent self.character
                                                                   new-character
                                                                   self.destroyed-characters))))]])
