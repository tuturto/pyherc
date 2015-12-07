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
