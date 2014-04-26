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
