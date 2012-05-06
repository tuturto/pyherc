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
Module for effect specification builder
"""
from pyherc.data import ItemEffectData

class EffectSpecBuilder(object):
    """
    Class for building effect specifications
    """
    def __init__(self):
        """
        Default constructor
        """
        super(EffectSpecBuilder, self).__init__()
        self.trigger = 'on drink'
        self.effect = 'heal'
        self.parameters = None
        self.charges = 1

    def with_trigger(self, trigger):
        self.trigger = trigger
        return self

    def with_effect(self, effect):
        self.effect = effect
        return self

    def with_parameters(self, parameters):
        self.parameters = parameters
        return self

    def with_charges(self, charges):
        self.charges = charges
        return self

    def build(self):
        """
        Build effect specification

        Returns:
            ItemEffectData
        """
        effect = ItemEffectData(trigger = self.trigger,
                                effect = self.effect,
                                parameters = self.parameters,
                                charges = self.charges)

        return effect
