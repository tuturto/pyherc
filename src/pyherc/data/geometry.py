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


def diagonals_around(location):
    """
    Get diagonal coordinates around location
    """
    loc_x, loc_y = location
    yield (loc_x - 1, loc_y - 1)
    yield (loc_x - 1, loc_y + 1)
    yield (loc_x + 1, loc_y - 1)
    yield (loc_x + 1, loc_y + 1)


def free_locations_around(level, location):
    """
    Get passable nodes around given location
    """
    # TODO: eventually remove this
    return [node for node in area_4_around(location)
            if not blocks_movement(level, location)]


def in_area(area_fn, location1, location2):
    return location2 in area_fn(location1)


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
