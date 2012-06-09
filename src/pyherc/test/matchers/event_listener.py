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
Module for event listener matchers used in testing
"""

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

class EventListeners(BaseMatcher):
    """
    Class to event listeners
    """
    def __init__(self, listener):
        """
        Default constructor
        """
        super(EventListeners, self).__init__()
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
        description.append(
                    'Object with event listener {0}'
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
