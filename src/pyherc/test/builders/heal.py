#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
Module for building heal related objects
"""
from pyherc.data.effects import Heal
from mockito import mock

class HealBuilder(object):
    """
    Class for building heal
    """
    def __init__(self):
        """
        Default constructor
        """
        super(HealBuilder, self).__init__()
        self.duration = 1
        self.frequency = 1
        self.tick = 0
        self.healing = 5
        self.target = mock()
        self.icon = 101
        self.title = 'healing'
        self.description = 'heals wounds'

    def with_duration(self, duration):
        """
        Set duration of heal

        :param duration: duration
        :type duration: int
        """
        self.duration = duration
        return self

    def with_frequency(self, frequency):
        """
        Set frequency of heal
        """
        self.frequency = frequency
        return self

    def with_tick(self, tick):
        """
        Set internal clock of heal
        """
        self.tick = tick
        return self

    def with_healing(self, healing):
        """
        Set healing amount
        """
        self.healing = healing
        return self

    def with_target(self, target):
        """
        Set target of the heal
        """
        self.target = target
        return self

    def build(self):
        """
        Builds heal object
        """
        return Heal(duration = self.duration,
                    frequency = self.frequency,
                    tick = self.tick,
                    healing = self.healing,
                    target = self.target,
                    icon = self.icon,
                    title = self.title,
                    description = self.description)
