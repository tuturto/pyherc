;; -*- coding: utf-8 -*-
;;
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

(require pyherc.test.cutesy.macros)

(import [pyherc.test.builders [ItemBuilder]])

(item LeatherArmour
      (.with-name "leather armour")
      (.with-damage-reduction 1)
      (.with-speed-modifier 1.0))

(item ScaleMail
      (.with-name "scale mail")
      (.with-damage-reduction 3)
      (.with-speed-modifier 0.7))

(item PlateMail
      (.with-name "plate mail")
      (.with-damage-reduction 5)
      (.with-speed-modifier 0.5))

(item LightBoots
      (.with-name "light boots")
      (.with-boots-damage-reduction 1)
      (.with-boots-speed-modifier 0.9))

(item HeavyBoots
      (.with-name "heavy boots")
      (.with-boots-damage-reduction 3)
      (.with-boots-speed-modifier 0.8))

(item IronBoots
      (.with-name "iron boots")
      (.with-boots-damage-reduction 4)
      (.with-boots-speed-modifier 0.75))
