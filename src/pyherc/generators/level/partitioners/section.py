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
Classes to represent division of levels
"""

class Section():
    """
    Class representing a single section in a level
    """
    def __init__(self, corner1, corner2, level, random_generator):
        """
        Default constructor

        :param corner1: Coordinates of first corner
        :type corner1: (integer, integer)
        :param corner2: Coordinates of the second corner
        :type corner2: (integer, integer)
        :param level: level where section is linked
        :type level: Level
        :param random_generator: random number generator
        :type random_generator: Random

        .. note:: Coordinates are given relative to level origo
        """
        super().__init__()

        self._corners = []
        self._corners.append(corner1)
        self._corners.append(corner2)
        self.level = level

        self._connections = []
        self._room_connections = []
        self._neighbours = []
        self.random_generator = random_generator
