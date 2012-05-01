#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
#
#   This file is part of pyherc.
#
#   pyherc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyherc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

"""
Module for healing
"""
from pyherc.aspects import Logged
from pyherc.rules.effects.effect import Effect

class Heal(Effect):
    """
    Class representing effects of healing
    """
    logged = Logged()

    @logged
    def __init__(self, duration, frequency, tick, healing, target):
        """
        Default constructor
        """
        super(Heal, self).__init__(duration, frequency, tick)
        self.healing = healing
        self.target = target

    @logged
    def do_trigger(self):
        """
        Triggers effects of the healing
        """
        self.target.hit_points = self.target.hit_points + self.healing
