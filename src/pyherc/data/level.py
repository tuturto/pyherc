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

        if size[0] != 0 and size[1] != 0:
            for loc_x in range(0, size[0] + 1):
                for loc_y in range(0, size[1] + 1):
                    floor_tile(self, (loc_x, loc_y), floor_type)
                    wall_tile(self, (loc_x, loc_y), wall_type)

        self._items = []
        self._characters = []

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
