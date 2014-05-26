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
Module containing classes to represent Level
"""

import random

from pyherc.aspects import log_debug
from pyherc.data.new_level import get_tile, floor_tile, wall_tile, get_portal
from pyherc.data.new_level import blocks_movement

class Level():
    """
    Represents a level
    """
    @log_debug
    def __init__(self, model, size=(0, 0), floor_type=None, wall_type=None):
        """
        Initialises a level of certain size and fills floor and walls with
        given types

        :param model: model to use
        :type model: Model
        :param size: optional size of the level
        :type size: (integer, integer)
        :param floor_type: type of floor to fill level
        :type floor_type: integer
        :param wall_type: type of wall to fill level
        :type wall_type: integer
        :empty_floor: type of floor for empty
        :type empty_floor: integer
        :empty_wall: type of wall for empty
        :type empty_wall: integer
        """
        super().__init__()

        self.model = model
        self.tiles = {}
        self.traps = []
        self.__location_type = []
        self.lit = []

        if size[0] != 0 and size[1] != 0:
            for loc_x in range(0, size[0] + 1):
                for loc_y in range(0, size[1] + 1):
                    floor_tile(self, (loc_x, loc_y), floor_type)
                    wall_tile(self, (loc_x, loc_y), wall_type)

            for loc_x in range(0, size[0] + 1):
                temp_row = []
                for loc_y in range(0, size[1] + 1):
                    temp_row.append(None)
                self.__location_type.append(temp_row)

            for loc_x in range(0, size[0] + 1):
                temp_row = []
                for loc_y in range(0, size[1] + 1):
                    temp_row.append([])
                self.traps.append(temp_row)

        self._items = []
        self._characters = []
        self.full_update_needed = True
        self.dirty_rectangles = []

    def add_trap(self, trap, location):
        """
        Add a trap to level

        :param trap: trap to add
        :type trap: Trap
        :param location: location to add the trap
        :type location: (int, int)

        .. versionadded:: 0.11
        """
        self.traps[location[0]][location[1]].append(trap)
        trap.location = location

    def get_traps(self, location):
        """
        Get traps at given location

        :param location: location to get traps from
        :type location: (int, int)
        :returns: list of traps
        :rtype: [Trap]

        .. versionadded:: 0.11
        """
        return self.traps[location[0]][location[1]]

    @log_debug
    def set_location_type(self, location, location_type):
        """
        Set type of location

        :param  location: location to set
        :type location: (integer, integer)
        :param location_type: type of location
        :type location_type: int
        """
        self.__location_type[location[0]][location[1]] = location_type

    def get_location_type(self, location):
        """
        Get type of location

        :param location: location to get
        :type location: (integer, integer)
        :returns: Type of location
        :rtype: int
        """
        return self.__location_type[location[0]][location[1]]

    def get_locations_by_type(self, location_type):
        """
        Get locations marked as rooms

        :param location_type: Type of location to search.
        :type location_type: string
        :returns: locations identifying rooms
        :rtype: [(int, int)]
        """
        rooms = []
        for loc_x in range(len(self.__location_type)):
            for loc_y in range(len(self.__location_type[0])):
                if (self.__location_type[loc_x][loc_y] == location_type or
                        self.__location_type[loc_x][loc_y] is not None
                        and location_type == 'any'):
                    rooms.append((loc_x, loc_y))

        return rooms

    def heuristic_estimate_of_distance(self, start, goal):
        """
        This should be >= 0
        If you want to be sure, that the found path is the sortest one,
        let this return a constant 0.
        """
        l = len(goal)
        return (sum([(start[i] - goal[i]) ** 2 for i in range(l)])) ** 0.5

    def neighbor_nodes(self, node):
        """
        node : the node of which neighbours you want to get
        It might also be a good choise to implement a class for the node
        """
        nodes = []
        loc_x = node[0]
        loc_y = node[1]

        if not blocks_movement(self, (loc_x - 1, loc_y)):
            nodes.append((loc_x - 1, loc_y))

        if not blocks_movement(self, (loc_x + 1, loc_y)):
            nodes.append((loc_x + 1, loc_y))

        if not blocks_movement(self, (loc_x, loc_y - 1)):
            nodes.append((loc_x, loc_y - 1))

        if not blocks_movement(self, (loc_x, loc_y + 1)):
            nodes.append((loc_x, loc_y + 1))

        return nodes

    def dist_between(self, start, goal):
        """
        The real distance between two adjacent nodes.
        This should be >= 0
        """
        l = len(goal)
        return (sum([(start[i] - goal[i]) ** 2 for i in range(l)])) ** 0.5

