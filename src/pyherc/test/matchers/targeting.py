# -*- coding: utf-8 -*-

#   Copyright 2010-2015 Tuukka Turto
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
Matchers for targeting
"""

from hamcrest.core.base_matcher import BaseMatcher


class TargetMatcher(BaseMatcher):
    """
    Class for checking target data
    """
    def __init__(self, target_type, location):
        """
        Default constructor
        """
        super().__init__()
        self.target_type = target_type
        self.location = location

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        if item.location != self.location:
            return False

        if item.target_type != self.target_type:
            return False

        return True

    def describe_to(self, description):
        """
        Describe this match
        """
        description.append('Targeting {0} at location {1}'
                           .format(self.target_type,
                                   self.location))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        mismatch_description.append('Was target of type {0} at location {1}'
                                    .format(item.target_type,
                                            item.location))


def wall_target_at(location):
    """
    Check that given target is at wanted wall
    """
    return TargetMatcher('wall', location)


def void_target():
    """
    Check that given target is nothing at all
    """
    return TargetMatcher('void', None)


def void_target_at(location):
    """
    Check that given target is nothign at all, but in given location
    """
    return TargetMatcher('void', location)
