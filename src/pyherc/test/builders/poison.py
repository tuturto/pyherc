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
Module for building poison related objects
"""
from mockito import mock
from pyherc.data.effects import Poison


class PoisonBuilder():
    """
    Class for building poison
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
        return Poison(duration=self.duration,
                      frequency=self.frequency,
                      tick=self.tick,
                      damage=self.damage,
                      target=self.target,
                      icon=self.icon,
                      title=self.title,
                      description=self.description)
