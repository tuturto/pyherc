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

(setv __doc__ "helper macros AIs")

(defmacro second [collection]
  (quasiquote (get (unquote collection) 1)))

(defmacro third [collection]
  (quasiquote (get (unquote collection) 2)))

(defmacro fourth [collection]
  (quasiquote (get (unquote collection) 3)))

(defmacro rarely [code else-code]
  (quasiquote (if (< (.randint random 1 100) 25) (unquote code)
		  (unquote else-code))))

(defmacro sometimes [code else-code]
  (quasiquote (if (< (.randint random 1 100) 50) (unquote code)
		  (unquote else-code))))

(defmacro often [code else-code]
  (quasiquote (if (< (.randint random 1 100) 75) (unquote code)
		  (unquote else-code))))
