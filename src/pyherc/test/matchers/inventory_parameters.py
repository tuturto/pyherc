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
Module for matching inventory action arguments
"""
from mockito.matchers import Matcher


class DropActionParameterMatcher(Matcher):
    """
    Matcher to check drop action parameters
    """
    def __init__(self, item):
        """
        Default constructor

        :param item: item to check
        :type item: Item
        """
        super().__init__()
        self.item = item

    def matches(self, arg):
        """
        Check if the passed argument matches

        :param arg: argument to check
        :returns: True if match, otherwise False
        :rtype: boolean
        """
        match_ok = True

        if arg.action_type != 'inventory':
            match_ok = False

        if arg.sub_action != 'drop':
            match_ok = False

        if arg.item != self.item:
            match_ok = False

        return match_ok

    def __repr__(self):
        """
        Get string explanation of this matcher

        :returns: explanation of expected match
        :rtype: string
        """
        return """action_type = 'inventory'
                  sub_action = 'drop'
                  item = {0}""".format(self.item)
