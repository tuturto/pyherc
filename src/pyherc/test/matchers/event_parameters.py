#!/usr/bin/env python3
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
Module for matching inventory action arguments
"""
from mockito.matchers import Matcher # pylint: disable=E0611

class EventType(Matcher):
    """
    Matcher to check event type

    .. versionadded:: 0.7
    """
    def __init__(self, type):
        """
        Default constructor

        :param type: type of event
        :type type: string
        """
        self.event_type = type

    def matches(self, arg):
        """
        Check if the passed argument matches

        :param arg: argument to check
        :returns: True if match, otherwise False
        :rtype: boolean
        """
        return arg.event_type == self.event_type

    def __repr__(self):
        """
        Get string explanation of this matcher

        :returns: explanation of expected match
        :rtype: string
        """
        return 'event_type: {0}'.format(self.event_type)
