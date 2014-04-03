#!/usr/bin/env python3
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
Module for end screen actions
"""
from pyherc.data.model import DIED_IN_DUNGEON, ESCAPED_DUNGEON


class EndScreenController():
    """
    Class for end screen actions

    .. versionadded:: 0.9
    """
    def __init__(self):
        """
        Default constructor
        """
        super(EndScreenController, self).__init__()

    def get_end_description(self, code):
        """
        Get textual explanation of end
        """
        if code == ESCAPED_DUNGEON:
            explanation = 'managed to escape alive'
        elif code == DIED_IN_DUNGEON:
            explanation = 'was killed in dungeon'
        else:
            explanation = 'got tired of living'

        return explanation
