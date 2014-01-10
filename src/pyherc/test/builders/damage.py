# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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
Module for building damage related objects
"""
from pyherc.data.effects import Damage
from mockito import mock

class DamageBuilder():
    """
    Class for building heal
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.duration = 1
        self.frequency = 1
        self.tick = 0
        self.damage = 5
        self.damage_type = 'magical'
        self.target = mock()
        self.icon = 101
        self.title = 'damage'
        self.description = 'causes wounds'

    def with_duration(self, duration):
        """
        Set duration of damage

        :param duration: duration
        :type duration: int
        """
        self.duration = duration
        return self

    def with_frequency(self, frequency):
        """
        Set frequency of damage
        """
        self.frequency = frequency
        return self

    def with_tick(self, tick):
        """
        Set internal clock of damage
        """
        self.tick = tick
        return self

    def with_damage(self, damage):
        """
        Set damage amount
        """
        self.damage = damage
        return self

    def with_target(self, target):
        """
        Set target of the damage
        """
        self.target = target
        return self

    def with_damage_type(self, damage_type):
        """
        Set type of damage
        """
        self.damage_type = damage_type
        return self

    def build(self):
        """
        Builds damage object
        """
        return Damage(duration = self.duration,
                      frequency = self.frequency,
                      tick = self.tick,
                      damage = self.damage,
                      damage_type = self.damage_type,
                      target = self.target,
                      icon = self.icon,
                      title = self.title,
                      description = self.description)
