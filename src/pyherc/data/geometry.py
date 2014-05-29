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
Module for various helpers
"""
from functools import partial
from math import sqrt
from pyherc.data.level import blocks_movement, get_character
from pyherc.aspects import log_debug


@log_debug
def get_target_in_direction(level, location, direction, attack_range=100):
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
    target_location = location
    target_data = None

    if direction == 9:
        return TargetData('void',
                          None,
                          None,
                          None)

    off_sets = [(0, 0),
                (0, -1), (1, -1), (1, 0), (1, 1),
                (0, 1), (-1, 1), (-1, 0), (-1, -1)]

    while (target is None
           and distance_between(location, target_location) <= attack_range):
        target_location = tuple([x for x in
                                 map(sum,
                                     zip(target_location,
                                         off_sets[direction]))])

        if blocks_movement(level, target_location):
            target_data = TargetData('wall',
                                     target_location,
                                     None,
                                     target_data)
            target = target_data
        else:
            target = get_character(level, target_location)
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
                                           attack_range=1.5)

def distance_between(location1, location2):
    """
    calculate distance between two points
    """
    if hasattr(location1, 'location'):
        loc1 = location1.location
    else:
        loc1 = location1

    if hasattr(location2, 'location'):
        loc2 = location2.location
    else:
        loc2 = location2

    x_difference = loc2[0] - loc1[0]
    y_difference = loc2[1] - loc1[1]

    return sqrt(x_difference**2 + y_difference**2)

def heuristic_estimate_of_distance(start, goal):
    """
    This should be >= 0
    If you want to be sure, that the found path is the sortest one,
    let this return a constant 0.
    """
    l = len(goal)
    return (sum([(start[i] - goal[i]) ** 2 for i in range(l)])) ** 0.5

def find_direction(start, end):
    """
    Find direction from start to end
    """
    if start[0] == end[0]:
        if start[1] < end[1]:
            return 5
        else:
            return 1
    elif start[1] == end[1]:
        if start[0] < end[0]:
            return 3
        else:
            return 7
    elif start[0] < end[0]:
        if start[1] < end[1]:
            return 4
        else:
            return 2
    elif start[0] > end[0]:
        if start[1] < end[1]:
            return 6
        else:
            return 8

@log_debug
def area_around(location):
    """
    Get coordinates for area around given location
    """
    for loc_x in range(location[0]-1, location[0]+2):
        for loc_y in range(location[1]-1, location[1]+2):
            if loc_x != location[0] or loc_y != location[1]:
                yield (loc_x, loc_y)


def area_4_around(location):
    """
    Get coordinates in cardinal directions around location
    """
    loc_x, loc_y = location
    yield (loc_x, loc_y - 1)
    yield (loc_x + 1, loc_y)
    yield (loc_x, loc_y + 1)
    yield (loc_x - 1, loc_y)

class TargetData():
    """
    Represents target

    .. versionadded:: 0.10
    """
    @log_debug
    def __init__(self, target_type, location, target, previous_target):
        """
        Default constructor
        """
        super().__init__()
        self.target_type = target_type
        self.location = location
        self.target = target
        self.previous_target = previous_target
