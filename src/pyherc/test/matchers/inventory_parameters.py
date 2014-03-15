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
