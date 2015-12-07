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
Module for event listener matchers used in testing
"""

from pyherc.events import e_event_type
from hamcrest.core.base_matcher import BaseMatcher


class EventRedraws(BaseMatcher):
    """
    Class for checking redraws in event
    """
    def __init__(self, redraws):
        """
        Default constructor
        """
        super().__init__()
        self.redraws = redraws

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        for redraw in self.redraws:
            if not redraw in item.affected_tiles:
                return False

        return True

    def describe_to(self, description):
        """
        Describe this match
        """
        description.append('Event with affected tiles {0}'
                           .format(self.redraws))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        mismatch_description.append('Was event with affected tiles {0}'
                                    .format(item.affected_tiles))


def has_marked_for_redrawing(redraws):
    """
    Check that item has given sections marked for redrawing
    """
    return EventRedraws(redraws)

