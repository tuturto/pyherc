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
Module for spell objects
"""

from pyherc.aspects import log_debug, log_info
from pyherc.data.effects import EffectsCollection


class Spell():
    """
    Class to represent spells

    .. versionadded:: 0.9
    """

    @log_debug
    def __init__(self):
        """
        Default constructor
        """
        self.targets = []
        self.effects = EffectsCollection()
        self.spirit = 0

    @log_debug
    def add_effect_handle(self, handle):
        """
        Add effect handle

        :param handle: effect handle to add
        :type handle: EffectHandle
        """
        self.effects.add_effect_handle(handle)

    @log_debug
    def get_effect_handles(self, trigger=None):
        """
        Get effect handles

        :param trigger: optional trigger type
        :type trigger: string

        :returns: effect handles
        :rtype: [EffectHandle]
        """
        return self.effects.get_effect_handles(trigger)

    @log_debug
    def remove_effect_handle(self, handle):
        """
        Remove given handle

        :param handle: handle to remove
        :type handle: EffectHandle
        """
        self.effects.remove_effect_handle(handle)

    @log_info
    def cast(self, effects_factory, dying_rules):
        """
        Cast the spell

        :param effects_factory: factory for creating effects
        :type effects_factory: EffectsFactory
        :param dying_rules: rules for dying
        :type dying_rules: Dying
        """
        handles = self.effects.get_effect_handles('on spell hit')
        effects = []

        targets = (x.target for x in self.targets
                   if x.target)

        for target in targets:
            for handle in handles:
                effects.append(effects_factory(key=handle.effect,
                                               target=target))

        for effect in effects:
            if not effect.duration or effect.duration <= 0:
                effect.trigger(dying_rules)
            else:
                effect.target.add_effect(effect)
