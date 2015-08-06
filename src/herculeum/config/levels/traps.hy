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

(require pyherc.config.dsl.traps)
(require herculeum.config.levels.macros)

(items-dsl)
(traps-dsl)

(traps ("pit" PitTrap)
       ("small caltrops" Caltrops "damage" 1 "icon" "caltrops")
       ("large caltrops" Caltrops "damage" 2 "icon" "caltrops"))

(items-list
 (trap-bag "bag of small caltrops"
           "a small bag filled with sharp caltrops"
           "small caltrops"
           1 150 1 ["bag"] ["trap bag"] "common")
 (trap-bag "greater bag of caltrops"
           "a rather large bag filled with sharp caltrops"
           "small caltrops"
           3 450 1 ["bag"] ["trap bag"] "uncommon")
 (trap-bag "bag of brutal caltrops"
           "a small bag of rather nasty looking caltrops"
           "large caltrops"
           1 250 1 ["bag"] ["trap bag"] "uncommon"))
