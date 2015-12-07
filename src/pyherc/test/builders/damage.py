# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Module for building damage related objects
"""
from mockito import mock
from pyherc.data.effects import DamageEffect


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
        return DamageEffect(duration=self.duration,
                            frequency=self.frequency,
                            tick=self.tick,
                            damage=self.damage,
                            damage_type=self.damage_type,
                            target=self.target,
                            icon=self.icon,
                            title=self.title,
                            description=self.description)
