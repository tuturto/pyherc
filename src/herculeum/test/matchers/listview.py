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
Module for matchers for ListView
"""

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

class ListViewItemMatcher(BaseMatcher):
    """
    Class to check list view item data

    .. versionadded:: 0.7
    """
    def __init__(self, title, description, icon):
        """
        Default constructor
        """
        super(ListViewItemMatcher, self).__init__()
        self.title = title
        self.description = description
        self.icon = icon

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        if not self.title.matches(item.title):
            return False

        if not self.description.matches(item.description):
            return False

        if not self.icon.matches(item.icon):
            return False

        return True

    def describe_to(self, description):
        """
        Describe this matcher
        """
        description.append('List view item, with title: {0}, description {1} and icon {2}'.format(self.title, self.description, self.icon))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        mismatch_description.append('List view item, with title: {0}, description {1} and icon {2}'.format(item.title, item.description, item.icon))

def is_showing(title = None, description = None, icon = None):
    """
    Check that list view item is showing correct data

    .. versionadded:: 0.7
    """
    if not hasattr(icon, 'matches'):
        icon_matcher = wrap_matcher(icon)
    else:
        icon_matcher = icon

    return ListViewItemMatcher(wrap_matcher(title),
                               wrap_matcher(description),
                               icon_matcher)
