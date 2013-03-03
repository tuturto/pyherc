#!/usr/bin/env python
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
Module for customer matchers used in testing
"""

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core import anything #pylint: disable-msg=E0611
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

class ContainsItem(BaseMatcher):
    """
    Class to check if given level has Items
    """
    def __init__(self, item, amount):
        """
        Default constructor
        """
        super(ContainsItem, self).__init__()
        self.item = item
        self.amount = amount

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
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

class HasDamage(BaseMatcher):
    """
    Class to check if item makes specific amount of specific damage
    """
    def __init__(self, damage_amount, damage_type):
        """
        Default constructor
        """
        super(HasDamage, self).__init__()
        self.damage_amount = damage_amount
        self.damage_type = damage_type

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        for damage in item.weapon_data.damage:
            if not self.damage_amount._matches(damage[0]):
                return False
            if not self.damage_type._matches(damage[1]):
                return False

        return True

    def describe_to(self, description):
        """
        Describe this matcher
        """
        description.append('Weapon making ')
        self.damage_amount.describe_to(description)
        description.append(' points of ')
        self.damage_type.describe_to(description)
        description.append(' damage')

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        mismatch_description.append('Was weapon with damage: {0}'.format(
                item.weapon_data.damage))

def does_have_item(item, amount = 1):
    """
    Check if level has given item

    :param item: name of the item to check
    :type item: String
    :param amount: amount of items to expect
    :type amount: int
    """
    return ContainsItem(item, wrap_matcher(amount))

def does_not_have_item(item):
    """
    Check that level does not have given item

    :param item: name of the item to check
    :type item: String
    """
    return ContainsItem(item, wrap_matcher(0))

def has_damage(damage_amount = None, damage_type = None):
    """
    Check if weapon makes specific amount and type of damage
    Both parameters support using matchers
    has_damage(greater_than(3), 'piercing') is valid call

    :param damage_amount: amount of damage
    :type damage_amount: int
    :param damage_type: type of damage
    :type damage_type: string
    """
    if damage_amount != None and damage_type != None:
        return HasDamage(wrap_matcher(damage_amount), wrap_matcher(damage_type))
    elif damage_amount == None:
        return HasDamage(anything(), wrap_matcher(damage_type))
    else:
        return HasDamage(wrap_matcher(damage_amount), anything())
