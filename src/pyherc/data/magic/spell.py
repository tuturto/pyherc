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
    def cast(self, effects_factory):
        """
        Cast the spell

        :param effects_factory: factory for creating effects
        :type effects_factory: EffectsFactory
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
                effect.trigger()
            else:
                effect.target.add_effect(effect)
