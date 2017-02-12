# -*- coding: utf-8 -*-

# Copyright (c) 2010-2017 Tuukka Turto
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
Module for general action related matchers
"""
from hamcrest.core.base_matcher import BaseMatcher


class ActionLegalityMatcher(BaseMatcher):
    """
    Matcher to check if action is legal
    """
    def __init__(self, should_be_legal):
        """
        Default constructor
        """
        super().__init__()
        self.should_be_legal = should_be_legal

    def _matches(self, item):
        """
        Check if matcher matches item

        :param item: object to match against
        :returns: True if matching, otherwise False
        :rtype: Boolean
        """
        if item.is_legal() == self.should_be_legal:
            return True
        else:
            return False

    def describe_to(self, description):
        """
        Describe this matcher
        """
        if self.should_be_legal:
            description.append('A legal action')
        else:
            description.append('An illegal action')

    def describe_mismatch(self, item, mismatch_description):
        """
        Describe this mismatch
        """

        if item.is_legal():
            mismatch_description.append('Legal action: {0}'.format(item))
        else:
            mismatch_description.append('Illegal action: {0}'.format(item))


def is_legal():
    """
    Check if action is legal
    """
    return ActionLegalityMatcher(True)


def is_illegal():
    """
    Check if action is illegal
    """
    return ActionLegalityMatcher(False)
