#!/usr/bin/env python3
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
Module for building poison related objects
"""
from pyherc.data.effects import Poison
from mockito import mock

class PoisonBuilder():
    """
    Class for building poison
    """
    def __init__(self):
        """
        Default constructor
        """
        super(PoisonBuilder, self).__init__()
        self.duration = 1
        self.frequency = 1
        self.tick = 0
        self.damage = 5
        self.target = mock()
        self.icon = 101
        self.title = 'poison'
        self.description = 'causes damage'

    def with_duration(self, duration):
        """
        Set duration of poison

        :param duration: duration
        :type duration: int
        """
        self.duration = duration
        return self

    def with_frequency(self, frequency):
        """
        Set frequency of poison
        """
        self.frequency = frequency
        return self

    def with_tick(self, tick):
        """
        Set internal clock of poison
        """
        self.tick = tick
        return self

    def with_damage(self, damage):
        """
        Set damage caused by poison
        """
        self.damage = damage
        return self

    def with_target(self, target):
        """
        Set target of the poison
        """
        self.target = target
        return self

    def build(self):
        """
        Builds poison object
        """
        return Poison(duration = self.duration,
                      frequency = self.frequency,
                      tick = self.tick,
                      damage = self.damage,
                      target = self.target,
                      icon = self.icon,
                      title = self.title,
                      description = self.description)
