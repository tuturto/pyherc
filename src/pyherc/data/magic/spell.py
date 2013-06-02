#!/usr/bin/env python3
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
Module for spell objects
"""

from pyherc.data.effects import EffectsCollection
from pyherc.aspects import logged

class Spell():
    """
    Class to represent spells
    
    .. versionadded:: 0.9
    """
    
    @logged
    def __init__(self):
        """
        Default constructor
        """
        self.target = []
        self.effects = EffectsCollection()

    @logged
    def add_effect_handle(self, handle):
        """
        Add effect handle

        :param handle: effect handle to add
        :type handle: EffectHandle
        """
        self.effects.add_effect_handle(handle)

    @logged
    def get_effect_handles(self, trigger = None):
        """
        Get effect handles

        :param trigger: optional trigger type
        :type trigger: string

        :returns: effect handles
        :rtype: [EffectHandle]
        """
        return self.effects.get_effect_handles(trigger)

    @logged
    def remove_effect_handle(self, handle):
        """
        Remove given handle

        :param handle: handle to remove
        :type handle: EffectHandle
        """
        self.effects.remove_effect_handle(handle)

    @logged
    def cast(self, effects_factory):
        """
        Cast the spell

        :param effects_factory: factory for creating effects
        :type effects_factory: EffectsFactory
        """
        handles = self.effects.get_effect_handles('on spell hit')
        effects = []

        for target in self.target:
            for handle in handles:
                effects.append(effects_factory.create_effect(
                                                key = handle.effect,
                                                target = target))

        #TODO: process effects
