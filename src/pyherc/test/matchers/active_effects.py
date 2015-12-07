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
        super().__init__()
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
        description.append('Object with {0} effects'
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
        super().__init__()
        self.effect = effect
        if effect is None:
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
            description.append('Object with effects containing {0}'
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


def has_effect(effect=None):
    """
    Check that item has given effect

    :param effect: effect instance to check
    :type effect: Effect
    """
    return EffectInstance(effect)
