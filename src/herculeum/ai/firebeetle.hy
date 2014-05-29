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

(setv __doc__ "module for AI routines for firebeetles")

(require pyherc.macros)
(import [herculeum.ai.patrol [patrol-ai]]
        [pyherc.data [open-area?]])

(defclass FireBeetleAI []
  [[__doc__ "AI routine for fire beetles"]
   [character None]
   [mode [:transit None]]
   [--init-- (fn [self character]
           "default constructor"
           (.--init-- (super FireBeetleAI self))
           (setv self.character character) None)]
   [act (fn [self model action-factory rng]
      "check the situation and act accordingly"
      (beetle-act self model action-factory))]])

(def beetle-act (patrol-ai open-area? 3))
