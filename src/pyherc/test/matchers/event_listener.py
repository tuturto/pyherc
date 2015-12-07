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

from hamcrest.core.base_matcher import BaseMatcher


class EventListeners(BaseMatcher):
    """
    Class to event listeners
    """
    def __init__(self, listener):
        """
        Default constructor
        """
        super().__init__()
        self.listener = listener

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        return self.listener in item.get_event_listeners()

    def describe_to(self, description):
        """
        Describe this match
        """
        description.append('Object with event listener {0}'
                           .format(self.listener))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        mismatch_description.append('Was object with listeners {0}'
                                    .format(item.get_event_listeners()))


def has_event_listener(listener):
    """
    Check if item has event listener
    """
    return EventListeners(listener)
