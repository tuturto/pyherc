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
Module for effects
"""
from pyherc.aspects import Logged

class EffectsFactory(object):
    """
    Factory for creating effects
    """
    logged = Logged()

    @logged
    def __init__(self):
        """
        Default constructor
        """
        super(EffectsFactory, self).__init__()
        self.effects = {}

    @logged
    def add_effect(self, key, type):
        """
        Add effect to internal dictionary

        Args:
            key: name of the effect
            type: type used for effect
        """
        self.effects[key] = type

    @logged
    def get_effect(self, key, **kwargs):
        """
        Instantiates new effect with given parameters

        Args:
            key: name of the effect
            kwargs: keyword arguments, passed to the effect
        """
        type = self.effects[key]
        return type(**kwargs)


class Effect(object):
    """
    Class representing effects
    """

    def __init__(self, duration, frequency):
        """
        Default constructor

        Args:
            duration: duration of the effect in ticks
            frequency: frequency of the effect in ticks
        """
        super(Effect, self).__init__()
        self.duration = duration
        self.frequency = frequency

class Poison(Effect):
    """
    Class representing effects of poison
    """
    logged = Logged()

    @logged
    def __init__(self, duration, frequency, damage, target):
        """
        Default constructor
        """
        super(Poison, self).__init__(duration, frequency)
        self.damage = damage
        self.target = target

    @logged
    def trigger(self):
        """
        Triggers effects of the poison
        """
        self.target.hit_points = self.target.hit_points - self.damage
