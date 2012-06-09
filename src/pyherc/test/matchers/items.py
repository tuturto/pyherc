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

from hamcrest import * #pylint: disable=W0401
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

class ContainsItem(BaseMatcher):
    """
    Class to check if given level has Items
    """
    def __init__(self, item, amount):
        """
        Default constructor
        """
        self.item = item
        self.amount = amount

    def _matches(self, item):
        """
        Check for match
        """
        count = 0

        for item in item.items:
            if item.name == self.item:
                count = count + 1

        return self.amount.matches(count)

    def describe_to(self, description):
        """
        Describe this matcher
        """
        if self.amount == None:
            description.append(
                    'Level with item named {0}'
                    .format(self.item))
        else:
            description.append(
                    'Level with {0} items named {1}'
                    .format(self.amount, self.item))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        names = [x.name for x in item.items]

        mismatch_description.append('Was level with items {0}'
                                    .format(names))

def does_have_item(item, amount):
    """
    Check if level has given item

    Args:
        item: Name of the item to check
        amount: Amount of items to expect
    """
    return ContainsItem(item, wrap_matcher(amount))
