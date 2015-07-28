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

(import [pyherc.data.traps [PitTrap Caltrops]]
        [pyherc.generators [get-trap-creator]]
        [hamcrest [assert-that instance-of]])

(defn setup []
  "setup test case"
  (let [[generator (get-trap-creator {"pit" [PitTrap {}]
                                      "caltrops" [Caltrops {"damage" 4}]})]]
    {:generator generator}))

(defn test-creating-trap []
  "creation of a trap is possible with trap creator"
  (let [[context (setup)]
        [generator (:generator context)]
        [trap (generator "pit")]]
    (assert-that trap (instance-of PitTrap))))

(defn test-creating-trap-with-parameters []
  "creationg of trap with parameters is possible"
  (let [[context (setup)]
        [generator (:generator context)]
        [trap (generator "caltrops")]]
    (assert-that trap (instance-of Caltrops))))
