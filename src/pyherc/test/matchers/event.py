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
Module for event listener matchers used in testing
"""

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
