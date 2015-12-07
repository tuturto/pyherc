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
Module for effect specification builder
"""
from pyherc.data.effects import Effect, EffectHandle


class EffectHandleBuilder():
    """
    Class for building effect specifications
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.trigger = 'on drink'
        self.effect = 'heal'
        self.parameters = None
        self.charges = 1
        self.icon = 0
        self.title = 'title'
        self.description = 'description'

    def with_trigger(self, trigger):
        """
        Configure effect handle to use specified trigger

        :param trigger: trigger to use
        :type trigger: string
        """
        self.trigger = trigger
        return self

    def with_effect(self, effect):
        """
        Configure effect handle to use specified effect

        :param effect: effect to create
        :type effect: Effect
        """
        self.effect = effect
        return self

    def with_parameters(self, parameters):
        """
        Configure effect handle with given parameters

        :param parameters: parameters to use when creating an effect
        """
        self.parameters = parameters
        return self

    def with_charges(self, charges):
        """
        Set amount of charges effect handle has

        :param charges: amount of charges
        :type charges: int
        """
        self.charges = charges
        return self

    def build(self):
        """
        Build effect specification

        Returns:
            EffectHandle
        """
        effect = EffectHandle(trigger=self.trigger,
                              effect=self.effect,
                              parameters=self.parameters,
                              charges=self.charges)

        return effect


class EffectBuilder():
    """
    Class to build effects
    """
    def __init__(self):
        super().__init__()
        self.duration = 0
        self.frequency = 0
        self.tick = 0
        self.effect_name = 'proto'
        self.multiple_allowed = False
        self.icon = 101
        self.title = 'effect'
        self.description = 'description'

    def with_duration(self, duration):
        """
        Set duration of the effect

        :param duration: duration in ticks
        :type duration: int
        """
        self.duration = duration
        return self

    def with_frequency(self, frequency):
        """
        Set frequency effect triggers

        :param frequency: frequency in ticks
        :type frequency: int
        """
        self.frequency = frequency
        return self

    def with_tick(self, tick):
        """
        Set internal clock of the effect

        :param tick: internal clock in ticks
        :type tick: int
        """
        self.tick = tick
        return self

    def with_effect_name(self, effect_name):
        """
        Set name of the effect

        :param effect_name: name to use
        :type effect_name: string
        """
        self.effect_name = effect_name
        return self

    def with_multiple_allowed(self):
        """
        Mark the effect to allow multiple instances
        """
        self.multiple_allowed = True
        return self

    def with_icon(self, icon):
        """
        Set icon for effect

        :param icon: icon to set
        :type icon: integer
        """
        self.icon = icon
        return self

    def with_title(self, title):
        """
        Set title for effect

        :param title: title to set
        :type title: string
        """
        self.title = title
        return self

    def with_description(self, description):
        """
        Set description for effect

        :param description: description to set
        :type description: string
        """
        self.description = description
        return self

    def build(self):
        """
        Build the effect

        :returns: fully configured effect
        :rtype: Effect
        """
        effect = Effect(duration=self.duration,
                        frequency=self.frequency,
                        tick=self.tick,
                        icon=self.icon,
                        title=self.title,
                        description=self.description)
        effect.effect_name = self.effect_name
        effect.multiple_allowed = self.multiple_allowed
        return effect
