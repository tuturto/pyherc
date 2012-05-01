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
Module for baseclass of every Effect
"""
from pyherc.aspects import Logged

class Effect(object):
    """
    Class representing effects
    """
    logged = Logged()

    def __init__(self, duration, frequency, tick):
        """
        Default constructor

        Args:
            duration: duration of the effect in ticks
            frequency: frequency of the effect in ticks
            tick: initial value for timer
        """
        super(Effect, self).__init__()
        self.duration = duration
        self.frequency = frequency
        self.tick = tick

    @logged
    def trigger(self):
        """
        Trigger the effect

        Note:
            This method will be called when tick reaches zero
        """
        self.do_trigger()
        self.post_trigger()

    @logged
    def do_trigger(self):
        """
        Override this method to contain logic of the effect
        """
        pass

    @logged
    def post_trigger(self):
        """
        Do house keeping after effect has been triggered
        """
        self.tick = self.frequency
        self.duration = self.duration - self.frequency
