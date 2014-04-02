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


class Level():
    """
    Represents a level
    """
    @log_debug
    def __init__(self, size=(0, 0), floor_type=None, wall_type=None,
                 empty_floor=0, empty_wall=0):
        """
        Initialises a level of certain size and fills floor and walls with
        given types

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

        self.floor = []
        self.walls = []
        self.ornamentations = []
        self.traps = []
        self.empty_floor = empty_floor
        self.empty_wall = empty_wall
        self.__location_type = []
        self.lit = []

        if size[0] != 0 and size[1] != 0:
            for loc_x in range(0, size[0] + 1):
                temp_row = []
                for loc_y in range(0, size[1] + 1):
                    temp_row.append(floor_type)
                self.floor.append(temp_row)

            for loc_x in range(0, size[0] + 1):
                temp_row = []
                for loc_y in range(0, size[1] + 1):
                    temp_row.append(wall_type)
                self.walls.append(temp_row)

            for loc_x in range(0, size[0] + 1):
                temp_row = []
                for loc_y in range(0, size[1] + 1):
                    temp_row.append(None)
                self.__location_type.append(temp_row)

            for loc_x in range(0, size[0] + 1):
                temp_row = []
                for loc_y in range(0, size[1] + 1):
                    temp_row.append(None)
                self.ornamentations.append(temp_row)

            for loc_x in range(0, size[0] + 1):
                temp_row = []
                for loc_y in range(0, size[1] + 1):
                    temp_row.append([])
                self.traps.append(temp_row)

        self.items = []
        self.portals = []
        self.creatures = []
        self.full_update_needed = True
        self.dirty_rectangles = []

    def get_tile(self, loc_x, loc_y):
        """
        Get tile at given location

        :param loc_x: x-coordinate of the location
        :type loc_x: integer
        :param loc_y: y-coordinate of the location
        :type loc_y: integer
        :returns: tile ID at given location
        :rtype: int
        """
        if loc_x < 0 or loc_y < 0:
            return self.empty_floor

        if loc_x > len(self.floor) or loc_y > len(self.floor[0]):
            return self.empty_floor

        if self.walls[loc_x][loc_y] != self.empty_wall:
            return self.walls[loc_x][loc_y]
        else:
            return self.floor[loc_x][loc_y]

    def get_wall_tile(self, loc_x, loc_y):
        """
        Get wall tile at given location

        :param loc_x: x-coordinate of the location
        :type loc_x: integer
        :param loc_y: y-coordinate of the location
        :type loc_y: integer
        :returns: wall tile ID at given location
        :rtype: int
        """
        if loc_x < 0 or loc_y < 0:
            return self.empty_wall

        if loc_x >= len(self.floor) or loc_y >= len(self.floor[0]):
            return self.empty_wall

        return self.walls[loc_x][loc_y]

    def set_wall_tile(self, loc_x, loc_y, tile):
        """
        Set wall tile at given location

        :param loc_x: x-coordinate of the location
        :type loc_x: integer
        :param loc_y: y-coordinate of the location
        :type loc_y: integer
        :param tile: tile to set
        :type tile: integer

        .. versionadded:: 0.10
        """
        if loc_x < 0 or loc_y < 0:
            return

        if loc_x >= len(self.floor) or loc_y >= len(self.floor[0]):
            return

        self.walls[loc_x][loc_y] = tile

    def get_floor_tile(self, loc_x, loc_y):
        """
        Get floor tile at given location

        :param loc_x: x-coordinate of the location
        :type loc_x: integer
        :param loc_y: y-coordinate of the location
        :type loc_y: integer
        :returns: floor tile ID at given location
        :rtype: int

        .. versionadded:: 0.10
        """
        if loc_x < 0 or loc_y < 0:
            return self.empty_floor

        if loc_x >= len(self.floor) or loc_y >= len(self.floor[0]):
            return self.empty_floor

        return self.floor[loc_x][loc_y]

    def set_floor_tile(self, loc_x, loc_y, tile):
        """
        Set floor tile at given location

        :param loc_x: x-coordinate of the location
        :type loc_x: integer
        :param loc_y: y-coordinate of the location
        :type loc_y: integer
        :param tile: tile to set
        :type tile: integer

        .. versionadded:: 0.10
        """
        if loc_x < 0 or loc_y < 0:
            return

        if loc_x >= len(self.floor) or loc_y >= len(self.floor[0]):
            return

        self.floor[loc_x][loc_y] = tile

    @log_debug
    def add_item(self, item, location):
        """
        Add an item to this level

        :param item: item to add
        :type item: Item
        :param location: location where to put the item
        :type location: (integer, integer)
        """
        assert item is not None
        assert location is not None

        self.items.append(item)
        item.location = location
        item.level = self

    def get_items_at(self, location):
        """
        Get list of items at location

        :param location: location to check
        :type location: (integer, integer)
        :returns: items at given location
        :rtype: [Item]
        """
        assert location is not None
        items = []
        for item in self.items:
            if item.location == location:
                items.append(item)
        return items

    @log_debug
    def add_portal(self, portal, location, other_end=None):
        """
        Adds precreated portal on level at given location
        If secondary portal is specified, link them together

        :param portal: portal to add
        :type portal: Portal
        :param location: location where to add portal
        :type location: (integer, integer)
        :param other_end: optional other end of the portal
        :type other_end: Portal
        """
        assert portal is not None
        assert location is not None

        portal.level = self
        portal.location = location
        self.set_floor_tile(portal.location[0],
                            portal.location[1],
                            portal.icon)

        self.portals.append(portal)

        if other_end is not None:
            assert(other_end.icon is not None or portal.icon is not None)

            portal.set_other_end(other_end)
            other_end.set_other_end(portal)

            #TODO: remove link
            if portal.icon is not None:
                if other_end.icon is None:
                    if portal.icon == 201:
                        other_end.icon = 200
                    else:
                        other_end.icon = 201
            else:
                if other_end.icon == 201:
                    portal.icon = 200
                else:
                    portal.icon = 201

    def get_portal_at(self, location):
        """
        Check if there is a portal at given location

        :param location: location of portal
        :type location: (integer, integer)
        :returns: Portal if found, otherwise None
        :rtype: Portal
        """
        for portal in self.portals:
            if portal.location == location:
                return portal

        return None

    @log_debug
    def add_creature(self, creature, location=None):
        """
        Add a creature to level

        :param creature: creature to add
        :type creature: Creature
        :param location: optional location for the creature
        :type location: (integer, integer)
        """
        assert creature is not None

        self.creatures.append(creature)
        creature.level = self
        if location is not None:
            creature.location = location

    @log_debug
    def remove_creature(self, creature):
        """
        Remove creature from level

        :param creature: creature to remove
        :type creature: Creature
        """
        assert creature is not None
        assert creature in self.creatures

        self.creatures.remove(creature)
        creature.level = None
        creature.location = ()

    def get_creature_at(self, location):
        """
        Get list of creatures at given location

        :param location: location to check
        :type location: (integer, integer)
        :returns: creature if found
        :rtype: Creature
        """
        assert location is not None
        for creature in self.creatures:
            if creature.location == location:
                return creature

        return None

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
    def find_free_space(self):
        """
        Finds free space where stuff can be placed

        :returns: Location where space is free
        :rtype: (int, int)
        """
        width = len(self.floor)
        height = len(self.floor[0])
        location = (random.randint(2, width - 1),
                    random.randint(2, height - 1))
        while self.walls[location[0]][location[1]] != self.empty_wall:
            location = (random.randint(2, width - 1),
                        random.randint(2, height - 1))
        return location

    def get_square(self, x_coordinate, y_coordinate):
        """
        Get square at given coordinates

        :param x_coordinate: x-coorinate of location
        :type x_coordinate: integer
        :param y_coordinate: y-coordinate of location
        :type y_coordinate: integer
        :returns: icon ID of the tile
        :rtype: int
        """
        if self.walls[x_coordinate][y_coordinate] != self.empty_wall:
            return self.walls[x_coordinate][y_coordinate]
        else:
            return self.floor[x_coordinate][y_coordinate]

    def blocks_movement(self, loc_x, loc_y):
        """
        Checks if there's movement blocking wall at given coordinates

        :param loc_x: x-coordinate of the location
        :type loc_x: integer
        :param loc_Y: y-coordinate of the location
        :type loc_y: integer
        :returns: True if location blocks regular movement, otherwise False
        :rtype: Boolean
        """
        if loc_x < 0 or loc_y < 0:
            return True

        if loc_x >= len(self.walls) or loc_y >= len(self.walls[0]):
            return True

        if self.walls[loc_x][loc_y] == self.empty_wall:
            return False
        else:
            return True

    def blocks_los(self, x_coordinate, y_coordinate):
        """
        Checks if there's LOS-blocking wall at given coordinates

        :param x_coordinate: x-coordinate of the location
        :type x_coordinate: integer
        :param y_coordinate: y-coordinate of the location
        :type y_coordinate: integer
        :returns: True if location blocks line of sight, otherwise False
        :rtype: Boolean
        """

        if x_coordinate < 0 or y_coordinate < 0:
            return True

        if (x_coordinate >= len(self.walls) or
                y_coordinate >= len(self.walls[0])):
            return True

        if self.walls[x_coordinate][y_coordinate] == self.empty_wall:
            return False
        else:
            return True

    @log_debug
    def get_size(self):
        """
        Gets size of level

        :returns: tupple, with width and length of level
        :rtype: (int, int)
        """
        x_size = len(self.floor)
        y_size = len(self.floor[0])

        return (x_size, y_size)

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

    def dump_string(self):
        """
        Dump this level into a string

        :returns: ascii representation of level
        :rtype: list of list
        """
        level_string = ""
        size = self.get_size()
        for loc_y in range(size[1]):
            level_string = level_string + '\n'
            for loc_x in range(size[0]):
                creature = self.get_creature_at((loc_x, loc_y))
                portal = self.get_portal_at((loc_x, loc_y))
                items = self.get_items_at((loc_x, loc_y))

                if creature is not None:
                    level_string = level_string + "X"
                elif portal is not None:
                    level_string = level_string + "<"
                elif len(items) > 0:
                    level_string = level_string + "*"
                elif self.walls[loc_x][loc_y] != self.empty_wall:
                    level_string = level_string + "#"
                elif self.walls[loc_x][loc_y] != self.empty_floor:
                    level_string = level_string + "."
                else:
                    level_string = level_string + " "
        return level_string

    def _repr_pretty_(self, p, cycle):
        """
        Pretty print for IPython
        """
        level_string = self.dump_string()

        if cycle:
            p.text('Level(...)')
        else:
            for char in level_string:
                if char != '\n':
                    p.text(char)
                else:
                    p.breakable()

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

        if not self.blocks_movement(loc_x - 1, loc_y):
            nodes.append((loc_x - 1, loc_y))

        if not self.blocks_movement(loc_x + 1, loc_y):
            nodes.append((loc_x + 1, loc_y))

        if not self.blocks_movement(loc_x, loc_y - 1):
            nodes.append((loc_x, loc_y - 1))

        if not self.blocks_movement(loc_x, loc_y + 1):
            nodes.append((loc_x, loc_y + 1))

        return nodes

    def dist_between(self, start, goal):
        """
        The real distance between two adjacent nodes.
        This should be >= 0
        """
        l = len(goal)
        return (sum([(start[i] - goal[i]) ** 2 for i in range(l)])) ** 0.5
