# -*- coding: utf-8 -*-

# Copyright (c) 2010-2017 Tuukka Turto
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
