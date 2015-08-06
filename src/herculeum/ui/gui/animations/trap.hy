;; -*- coding: utf-8 -*-

;;   Copyright 2010-2015 Tuukka Turto
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

(require pyherc.macros)

(import [herculeum.ui.gui.animations.animation [Animation]]
        [herculeum.ui.gui.layers [zorder_trap]]
        [pyherc.events [e-trap]])

(defclass PlaceTrapAnimation [Animation]
  "Generic animation for placing trap"
  [[--init-- (fn [self event]
               (super-init event)
               (setv self.trap (e-trap event))
               nil)]
   [trigger (fn [self ui]
              (.add-glyph ui self.trap
                          ui.scene
                          zorder-trap))]])
