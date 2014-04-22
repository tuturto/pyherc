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
Module for common constants
"""


class Duration():
    """
    Constants for time durations

    .. versionadded:: 0.10
    """
    instant = 1
    fast = 2
    normal = 4
    slow = 8
    very_slow = 16


class SpecialTime():
    """
    Constants for special occasions

    .. versionadded:: 0.10
    """
    aprilfools = 1
    christmas = 2


class Direction():
    """
    Constants for directions

    .. versionadded:: 0.10
    """
    north = 1
    north_east = 2
    east = 3
    south_east = 4
    south = 5
    south_west = 6
    west = 7
    north_west = 8
    enter = 9
