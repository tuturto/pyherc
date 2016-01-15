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
        if (item is not None
                and hasattr(item, 'item')
                and item.item is not None
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
