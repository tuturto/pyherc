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
Module for customer matchers used in testing
"""

from hamcrest import * #pylint: disable=W0401
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

class ContainsEffectHandle(BaseMatcher):
    """
    Class to check if given collection has effect handles
    """
    def __init__(self, handle):
        """
        Default constructor
        """
        if hasattr(handle, '__iter__'):
            self.handles = handle
        else:
            self.handles = [handle]

    def _matches(self, item):
        """
        Check for match
        """
        handles = item.get_effect_handles()

        for handle in self.handles:
            if not handle in handles:
                return False

        return True

    def describe_to(self, description):
        """
        Describe this matcher
        """
        description.append('Collection with handles {0}'
                           .format(self.handles))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        handles = item.get_effect_handles()

        mismatch_description.append('Was collection with handles {0}'
                                    .format(handles))

def has_effect_handle(handle):
    """
    Check if collection has the handle

    Args:
        handle: handle to expect
    """
    return ContainsEffectHandle(handle)

def has_effect_handles(handle):
    """
    Check if collection has all the handles

    Args:
        list of handles to expect
    """
    return ContainsEffectHandle(handle)
