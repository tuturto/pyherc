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
Module for customer matchers used in testing
"""

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

class Effects(BaseMatcher):
    """
    Class to check amount of active effects
    """
    def __init__(self, amount_of_effects):
        """
        Default constructor
        """
        super(Effects, self).__init__()
        self.amount_of_effects = amount_of_effects

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        return self.amount_of_effects.matches(len(item.get_effects()))

    def describe_to(self, description):
        """
        Describe this matcher
        """
        description.append(
                    'Object with {0} effects'
                    .format(self.amount_of_effects))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        mismatch_description.append('Was object with {0} effects'
                                    .format(len(item.get_effects())))

class EffectInstance(BaseMatcher):
    """
    Class to check amount of effects
    """
    def __init__(self, effect):
        """
        Default constructor
        """
        super(EffectInstance, self).__init__()
        self.effect = effect
        if effect == None:
            self.match_any = True
        else:
            self.match_any = False

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        if self.match_any:
            if len(item.get_effects()) > 0:
                return True
            else:
                return False

        for effect in item.get_effects():
            if effect == self.effect:
                return True
        return False

    def describe_to(self, description):
        """
        Describe this matcher
        """
        if self.match_any:
            description.append('Object with any effect')
        else:
            description.append(
                    'Object with effects containing {0}'
                    .format(self.effect))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        mismatch_description.append('Was object with effects {0}'
                                    .format(item.get_effects()))

def has_effects(amount_of_effects):
    """
    Check if item has effects
    :param amount_of_effects: amount of effects item should have
    :type amount_of_effects: int
    """
    return Effects(wrap_matcher(amount_of_effects))

def has_no_effects():
    """
    Check that item has no effects
    """
    return Effects(wrap_matcher(0))

def has_effect(effect = None):
    """
    Check that item has given effect

    :param effect: effect instance to check
    :type effect: Effect
    """
    return EffectInstance(effect)
