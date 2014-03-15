# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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


class ContainsEffectHandle(BaseMatcher):
    """
    Class to check if given collection has effect handles
    """
    def __init__(self, handle):
        """
        Default constructor
        """
        super().__init__()
        if handle is not None:
            self.match_any = False
            if hasattr(handle, '__iter__'):
                self.handles = handle
            else:
                self.handles = [handle]
        else:
            self.match_any = True
            self.handles = []

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        handles = item.get_effect_handles()

        if self.match_any:
            if len(handles) > 0:
                return True
            else:
                return False

        for handle in self.handles:
            if not handle in handles:
                return False

        return True

    def describe_to(self, description):
        """
        Describe this matcher
        """
        if self.match_any:
            description.append('Collection with any handle')
        else:
            description.append('Collection with handles {0}'
                               .format(self.handles))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        handles = item.get_effect_handles()

        mismatch_description.append('Was collection with handles {0}'
                                    .format(handles))


def has_effect_handle(handle=None):
    """
    Check if collection has the handle

    :param handle: handle to expect
    :type handle: EffectHandle

    .. note:: If left empty, any handle will match
    """
    return ContainsEffectHandle(handle)


def has_effect_handles(handle):
    """
    Check if collection has all the handles

    :param handle: list of handles to expect
    :type handle: []
    """
    return ContainsEffectHandle(handle)
