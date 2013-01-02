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

class PathFinding(BaseMatcher):
    """
    Helper class used to verify if generated path is connected and does
    not pass any walls
    """
    def __init__(self, start, destination, level):
        """
        Initialise this matcher
        """
        super(PathFinding, self).__init__()
        self.start = start
        self.destination = destination
        self.level = level
        self.fail_reason = None

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        if item[0] != self.start:
            self.fail_reason = 'path does not start from beginning'
            return False

        if item[-1] != self.destination:
            self.fail_reason = 'path does not reach destination'
            return False

        prev_loc = item[0]

        for loc in item[1:]:
            distance = ((loc[0] - prev_loc[0]) ** 2 +
                       (loc[1] - prev_loc[1]) ** 2) ** 0.5
            if distance > 1.42:
                self.fail_reason = 'path is not connected'
                return False
            prev_loc = loc

        return True

    def describe_to(self, description):
        """
        Describe this matcher
        """
        description.append(
                'Path going starting from {0} and ending to {1}'.format(
                                                    self.start,
                                                    self.destination))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        mismatch_description.append(self.fail_reason)

def continuous_path(start, destination, level):
    """
    check if path is continuous and does not pass walls
    """
    return PathFinding(start, destination, level)
