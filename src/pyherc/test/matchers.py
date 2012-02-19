#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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
from hamcrest.core.helpers.hasmethod import hasmethod
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

class MapConnectivity(BaseMatcher):
    """
    Metcher used to verify if generated level is fully connected
    """
    def __init__(self, level):
        """
        Initialise this matcher

        Args:
            level: Level to check for connectivity
        """
        self.level = level
        self.connectivity = None

    def _matches(self, item):
        """
        Find out if this Level is fully connected

        Returns:
            True if fully connected, otherwise False
        """
        self.connectivity = False
        return False

    def describe_to(self, description):
        """
        Describe this match
        """
        if self.connectivity == False:
            description.append("Not connected")
        else:
            description.append("Connected")

def whole_map_is_accessible_in(match):
    """
    Check that the map is fully connected

    Args:
        match: Level to check
    """
    return MapConnectivity(wrap_matcher(match))
