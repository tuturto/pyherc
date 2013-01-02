#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
Package for custom hamcrest matchers for ItemGlyph
"""

from hamcrest.core.base_matcher import BaseMatcher

class ItemGlyphMatcher(BaseMatcher):
    """
    Class to check ItemGlyph
    """
    def __init__(self, item_name):
        """
        Default constructor
        """
        super(ItemGlyphMatcher, self).__init__()
        self.item_name = item_name

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        if (item != None
                and hasattr(item, 'item')
                and item.item != None
                and item.item.name == self.item_name):
            return True
        else:
            return False

    def describe_to(self, description):
        """
        Describe this matcher
        """
        description.append('Item glyph with item named {0}'.format(self.item_name))

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """
        mismatch_description.append('Was object {0}'.format(item))

def slot_with_item(item_name):
    """
    Create hamcrest matcher that can check for existence of correctly named
    item in ItemGlyph
    """
    return ItemGlyphMatcher(item_name)
