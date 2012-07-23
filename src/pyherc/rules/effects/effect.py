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
Module for baseclass of every Effect
"""
from pyherc.aspects import Logged
from pyherc.events import Event

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
        self.effect_name = 'effect'

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

    @logged
    def get_add_event(self):
        """
        Get event describing adding of this effect

        :returns: event describing adding of this effect
        :rtype: Event
        """
        return Event(level = None,
                     location = None,
                     affected_tiles = [])

    @logged
    def get_removal_event(self):
        """
        Get event describing removal of this event

        :return: event describing removal of this event
        :rtype: Event
        """
        return Event(level = None,
                     location = None,
                     affected_tiles = [])

class EffectHandle(object):
    """
    Handle that can be used to construct effects

    Args:
        trigger: name of the trigger of the effect
        effect: name of the effect
        parameters: overriding parameters for the effect
        charges: amount of charges effect has
    """
    def __init__(self, trigger, effect, parameters, charges):

        self.trigger = trigger
        self.effect = effect
        self.parameters = parameters
        self.charges = charges

    def __str__(self):
        """
        String representation of this object
        """
        return "trigger: {0}, effect: {1}, parameters: {2}, charges: {3}".format(
            self.trigger, self.effect, self.parameters, self.charges)
