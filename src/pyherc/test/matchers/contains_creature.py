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

class ContainsCreature(BaseMatcher):
    """
    Class to check if given level has creatures
    """
    def __init__(self, creature, amount):
        """
        Default constructor
        """
        self.creature = creature
        self.amount = amount

    def _matches(self, item):
        """
        Check for match
        """
        count = 0

        for creature in item.creatures:
            if creature.name == self.creature:
                count = count + 1

        return self.amount.matches(count)

    def describe_to(self, description):
        """
        Describe this matcher
        """
        if self.amount == None:
            description.append(
                    'Level with creature named {0}'
                    .format(self.creature))
        else:
            description.append(
                    'Level with {0} creatures named {1}'
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

    Args:
        creature: Name of the creature to check
        amount: Amount of creatures to expect
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
        self.level = level
        self.item = None

    def _matches(self, item):
        """
        Check for match
        """
        count = 0
        self.item = item

        if item in self.level.creatures:
            return True
        else:
            return False

    def describe_to(self, description):
        """
        Describe this matcher
        """
        description.append(
                'Level with monster named {0}'
                .format(self.item))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        mismatch_description.append('Was level with creatures {0}'
                                    .format(self.level.creatures))

def is_at(level):
    """
    Check that level does have given creature
    """
    return IsLocatedIn(level)

def is_not_at(level):
    """
    Check that level does not have given creature
    """
    return is_not(IsLocatedIn(level))
