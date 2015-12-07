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


class PathFinding(BaseMatcher):
    """
    Helper class used to verify if generated path is connected and does
    not pass any walls
    """
    def __init__(self, start, destination, level):
        """
        Initialise this matcher
        """
        super().__init__()
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
        description.append('Path going starting from {0} and ending to {1}'
                           .format(self.start,
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
