#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
Module for damage modifiers
"""
from pyherc.aspects import Logged
from pyherc.data.effects.effect import Effect

class DamageModifier(Effect):
    """
    Class representing damage modifier

    .. versionadded:: 0.7
    """
    logged = Logged()

    @logged
    def __init__(self, modifier, damage_type, duration, frequency, tick):
        """
        Default constructor
        """
        super(DamageModifier, self).__init__(duration, frequency, tick)
        self.modifier = modifier
        self.damage_type = damage_type
        self.effect_name = 'damage modifier'
        self.multiple_allowed = True

    def clone(self):
        """
        Temporary hack for tech day
        """
        return DamageModifier(self.modifier, self.damage_type,
                              self.duration, self.frequency,
                              self.tick)