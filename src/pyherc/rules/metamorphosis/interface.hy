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
(require pyherc.macros)
(import [pyherc.rules.public [ActionParameters]]
	[pyherc.aspects [log-debug log-info]])

(defn morph [character new-character-name action-factory
             &optional [destroyed-characters #t()]]
  "perform morph on a character"
  (let [[action (.get-action action-factory
				(MetamorphosisParameters character 
                                                         new-character-name
                                                         destroyed-characters))]]
    (when (.legal? action)
      (.execute action))))

(defn morph-legal? [character new-character-name action-factory
                    &optional [destroyed-characters #t()]]
  "can morph be performed"
  (let [[action (.get-action action-factory
                             (MetamorphosisParameters character
                                                      new-character-name
                                                      destroyed-characters))]]
    (.legal? action)))

(defclass MetamorphosisParameters [ActionParameters]
  "Class controlling creation of MorphAction"
  [[--init-- #d(fn [self character new-character-name destroyed-characters]
		 (-> (super) (.--init--))
		 (setv self.action-type "metamorphosis")
		 (setv self.character character)
                 (setv self.new-character-name new-character-name)
                 (setv self.destroyed-characters destroyed-characters)
		 nil)]])
