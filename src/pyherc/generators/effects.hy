;; -*- coding: utf-8 -*-

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

(import [functools [partial]])
(import [copy [deepcopy]])
(import [pyherc.aspects [log-debug log-info]])
(require pyherc.aspects)
(require hy.contrib.anaphoric)

#i(defn get-effect-creator [effect-config]
    "get a function to create effects"
    (partial create-effect effect-config))

#d(defn create-effect [effect-config key &kwargs kwargs]
    "instantiates new effect with given parameters"
    (let [[config (get effect-config key)]
	  [params (deepcopy config)]
	  [effect-type (.pop params "type")]]
      (if params
	(ap-each kwargs (do
			 (when (in it params) (.pop params it))
			 (assoc params it (get kwargs it))))
	(setv params kwargs))
      (apply effect-type [] params)))
