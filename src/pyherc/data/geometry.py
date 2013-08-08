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
Module for various helpers
"""
from pyherc.aspects import logged
from math import sqrt

@logged
def get_target_in_direction(level, location, direction):
    """
    Get target of the attack

    :param level: level to operate
    :type level: Level
    :param location: start location
    :type location: (int, int)
    :param direction: direction to follow
    :type direction: int
    :returns: target character if found, otherwise None
    :rtype: Character
    """
    target = None
    off_sets = [(0, 0),
                (0, -1), (1, -1), (1, 0), (1, 1),
                (0, 1), (-1, 1), (-1, 0), (-1, -1)]

    while target == None and not level.blocks_movement(location[0], location[1]):
        location = tuple([x for x in
                          map(sum, zip(location, off_sets[direction]))])
        target = level.get_creature_at(location)

    return target

@logged
def distance_between(location1, location2):
    """
    calculate distance between two points
    """
    x_difference = location2[0] - location1[0]
    y_difference = location2[1] - location1[1]

    return sqrt(x_difference**2 + y_difference**2)
