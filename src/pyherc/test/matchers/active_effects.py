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
Module for customer matchers used in testing
"""

from hamcrest import * #pylint: disable=W0401
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

class ActiveEffects(BaseMatcher):
    """
    Class to check amount of active effects
    """
    def __init__(self, amount_of_effects):
        """
        Default constructor
        """
        self.amount_of_effects = amount_of_effects

    def _matches(self, item):
        return self.amount_of_effects.matches(len(item.active_effects))

    def describe_to(self, description):
        description.append(
                    'Object with {0} active effects'
                    .format(self.amount_of_effects))

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append('Was object with {0} active effects'
                                    .format(len(item.active_effects)))

class ActiveEffectInstance(BaseMatcher):
    """
    Class to check amount of active effects
    """
    def __init__(self, effect):
        """
        Default constructor
        """
        self.effect = effect

    def _matches(self, item):
        for effect in item.active_effects:
            if effect == self.effect:
                return True
        return False

    def describe_to(self, description):
        description.append(
                    'Object with active effects containing {0}'
                    .format(self.effect))

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append('Was object with active effects {0}'
                                    .format(item.active_effects))

def has_active_effects(amount_of_effects):
    return ActiveEffects(wrap_matcher(amount_of_effects))

def has_no_active_effects():
    return ActiveEffects(wrap_matcher(0))

def has_active_effect(effect):
    return ActiveEffectInstance(effect)
