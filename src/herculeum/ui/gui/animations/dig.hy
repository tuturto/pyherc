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

(import [herculeum.ui.gui.animations.animation [Animation]]
	[herculeum.ui.gui [layers]])

(defclass ExhumeAnimation [Animation]
  "animation for exhuming a grave"
  [[--init-- (fn [self event]
	       (-> (super) (.--init-- event))
	       (setv self.character event.character)
               (setv self.items event.new-items)
               (setv self.characters event.new-characters)
	       nil)]
   [trigger (fn [self ui]
              (ap-each self.items (.add-glyph ui it ui.scene
                                              layers.zorder-item))
              (ap-each self.characters (.add-glyph ui it ui.scene
                                                   layers.zorder-character)))]])
