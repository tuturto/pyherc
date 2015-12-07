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
Module for custom matchers used in testing
"""
from hamcrest.core.base_matcher import BaseMatcher


class IsWearingMatcher(BaseMatcher):
    """
    Matcher to check if character is wearing an item
    """
    def __init__(self, item, slot):
        """
        Default constructor
        """
        super().__init__()
        self.item = item
        self.slot = slot

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        inventory = item.inventory

        if self.slot == 'armour' and inventory.armour == self.item:
            return True

        if self.slot == 'boots' and inventory.boots == self.item:
            return True

        return False

    def describe_to(self, description):
        """
        Describe this matcher
        """
        description.append('Character wearing item {0}'.format(self.item))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        mismatch_description.append('Character with inventory {0}'
                                    .format(item.inventory))


class IsInInventoryMatcher(BaseMatcher):
    """
    Matcher to check if character has item in inventory
    """
    def __init__(self, item):
        """
        Default constructor
        """
        super().__init__()
        self.item = item

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        return self.item in item.inventory

    def describe_to(self, description):
        """
        Describe this matcher
        """
        description.append('Character carrying item {0}'.format(self.item))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        mismatch_description.append('Character with inventory {0}'
                                    .format(item.inventory))


def is_wearing_armour(item):
    """
    Check if character is wearing an item
    """
    return IsWearingMatcher(item, 'armour')

def is_wearing_boots(item):
    """
    Check if character is wearing boots
    """
    return IsWearingMatcher(item, 'boots')

def does_have(item):
    """
    Check if character has the item in inventory
    """
    return IsInInventoryMatcher(item)
