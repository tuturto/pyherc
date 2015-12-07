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

from hamcrest import is_not
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from pyherc.data import get_characters


class ContainsCreature(BaseMatcher):
    """
    Class to check if given level has creatures
    """
    def __init__(self, creature, amount):
        """
        Default constructor
        """
        super().__init__()
        self.creature = creature
        self.amount = amount

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        count = 0

        for creature in get_characters(item):
            if creature.name == self.creature:
                count = count + 1

        return self.amount.matches(count)

    def describe_to(self, description):
        """
        Describe this matcher
        """
        if self.amount is None:
            description.append('Level with creature named {0}'
                               .format(self.creature))
        else:
            description.append('Level with {0} creatures named {1}'
                               .format(self.amount, self.creature))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        names = [x.name for x in item.creatures]

        mismatch_description.append('Was level with creatures {0}'
                                    .format(names))


def has_creature(creature, amount):
    """
    Check if level has given creature

    :param creature: name of the creature to check
    :type creature: String
    :param amount: amount of creatures to expect
    :type amount: int
    """
    return ContainsCreature(creature, wrap_matcher(amount))


class IsLocatedIn(BaseMatcher):
    """
    Class to check if given level has creatures
    """
    def __init__(self, level):
        """
        Default constructor
        """
        super().__init__()
        self.level = level
        self.item = None

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        self.item = item

        if item in get_characters(self.level):
            return True
        else:
            return False

    def describe_to(self, description):
        """
        Describe this matcher
        """
        description.append('Level with monster named {0}'
                           .format(self.item))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        mismatch_description.append('Was level with creatures {0}'
                                    .format(get_characters(self.level)))


def is_in(level):
    """
    Check that level does have given creature
    """
    return IsLocatedIn(level)


def is_not_in(level):
    """
    Check that level does not have given creature
    """
    return is_not(IsLocatedIn(level))
