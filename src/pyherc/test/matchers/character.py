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

class AliveStatus(BaseMatcher):
    """
    Class to check if character is alive or not
    """
    def __init__(self, alive):
        """
        Default constructor
        """
        super(AliveStatus, self).__init__()
        self.alive = alive

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        if item.hit_points > 0:
            is_alive = True
        else:
            is_alive = False

        return is_alive == self.alive

    def describe_to(self, description):
        """
        Describe this matcher
        """
        if self.alive == True:
            description.append('Character who is alive')
        else:
            description.append('Character who is dead')

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        mismatch_description.append('Was character with {0} hit points'
                                    .format(item.hit_points))

def is_dead():
    """
    Check that character is dead
    """
    return AliveStatus(False)
