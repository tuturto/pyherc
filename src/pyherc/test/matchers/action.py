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
