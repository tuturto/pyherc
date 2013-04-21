#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
Module for custom matchers used in testing
"""
from hamcrest.core.base_matcher import BaseMatcher

class IsWearingMatcher(BaseMatcher):
    """
    Matcher to check if character is wearing an item
    """
    def __init__(self, item):
        """
        Default constructor
        """
        super(IsWearingMatcher, self).__init__()
        self.item = item

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        inventory = item.inventory

        if inventory.armour == self.item:
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
        mismatch_description.append('Character with inventory {0}'.format(
                item.inventory))

class IsInInventoryMatcher(BaseMatcher):
    """
    Matcher to check if character has item in inventory
    """
    def __init__(self, item):
        """
        Default constructor
        """
        super(IsInInventoryMatcher, self).__init__()
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
        mismatch_description.append('Character with inventory {0}'.format(
                item.inventory))

def is_wearing(item):
    """
    Check if character is wearing an item
    """
    return IsWearingMatcher(item)

def does_have(item):
    """
    Check if character has the item in inventory
    """
    return IsInInventoryMatcher(item)
