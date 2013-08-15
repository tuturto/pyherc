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
from functools import partial

@logged
def get_target_in_direction(level, location, direction, attack_range = 100):
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
    target_type = 'void'
    target_location = location
    range_covered = 1
    target_data = None

    if direction == 9:
        return TargetData('void',
                          None,
                          None,
                          None)

    off_sets = [(0, 0),
                (0, -1), (1, -1), (1, 0), (1, 1),
                (0, 1), (-1, 1), (-1, 0), (-1, -1)]

    while (target == None
           and distance_between(location, target_location) <= attack_range):
        target_location = tuple([x for x in
                                 map(sum,
                                     zip(target_location,
                                         off_sets[direction]))])

        if level.blocks_movement(target_location[0], target_location[1]):
            target_data = TargetData('wall',
                                     target_location,
                                     None,
                                     target_data)
            target = target_data
        else:
            target = level.get_creature_at(target_location)
            if target:
                target_data = TargetData('character',
                                         target_location,
                                         target,
                                         target_data)
                target = target_data
            else:
                target_data = TargetData('void',
                                         target_location,
                                         None,
                                         target_data)

    return target_data

get_adjacent_target_in_direction = partial(get_target_in_direction,
                                           attack_range = 1.5)

def distance_between(location1, location2):
    """
    calculate distance between two points
    """
    x_difference = location2[0] - location1[0]
    y_difference = location2[1] - location1[1]

    return sqrt(x_difference**2 + y_difference**2)

class TargetData():
    """
    Represents target

    .. versionadded:: 0.10
    """
    def __init__(self, target_type, location, target, previous_target):
        """
        Default constructor
        """
        super().__init__()
        self.target_type = target_type
        self.location = location
        self.target = target
        self.previous_target = previous_target