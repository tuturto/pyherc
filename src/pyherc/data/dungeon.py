#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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
Module containing classes to represent dungeon

Classes:
    Level
    Dungeon
    Portal
"""

import random
import logging
import pyherc.data.tiles
from pyherc.aspects import Logged

class Level(object):
    """
    Represents a level
    """
    __logger_name__ = 'pyherc.data.dungeon.Level'

    @Logged(__logger_name__)
    def __init__(self, size = (0, 0), floor_type = None, wall_type = None):
        """
        Initialises a level of certain size and fill floor and walls with given types
        """
        super(Level, self).__init__()
        self.logger = logging.getLogger('pyherc.data.dungeon.Level')

        self.floor = []
        self.walls = []
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

        self.items = []
        self.portals = []
        self.creatures = []
        self.full_update_needed = True
        self.dirty_rectangles = []

    def __getstate__(self):
        """
        Override __getstate__ in order to get pickling work
        """
        properties = dict(self.__dict__)
        del properties['logger']
        return properties

    def __setstate__(self, properties):
        """
        Override __setstate__ in order to get pickling work
        """
        self.__dict__.update(properties)
        self.logger = logging.getLogger('pyherc.data.dungeon.Level')

    def get_tile(self, loc_x, loc_y):
        """
        Get tile at given location

        Args:
            loc_x: x-coordinate of the location
            loc_y: y-coordinate of the location
        """
        if loc_x < 0 or loc_y < 0:
            return pyherc.data.tiles.FLOOR_EMPTY

        if loc_x > len(self.floor) or loc_y > len(self.floor[0]):
            return pyherc.data.tiles.FLOOR_EMPTY

        if self.walls[loc_x][loc_y] != pyherc.data.tiles.WALL_EMPTY:
            return self.walls[loc_x][loc_y]
        else:
            return self.floor[loc_x][loc_y]

    def get_wall_tile(self, loc_x, loc_y):
        """
        Get wall tile at given location

        Args:
            loc_x: x-coordinate of the location
            loc_y: y-coordinate of the location
        """
        if loc_x < 0 or loc_y < 0:
            return pyherc.data.tiles.WALL_GROUND

        if loc_x > len(self.floor) or loc_y > len(self.floor[0]):
            return pyherc.data.tiles.WALL_GROUND

        return self.walls[loc_x][loc_y]

    @Logged(__logger_name__)
    def add_item(self, item, location):
        """
        Add an item to this level

        Args:
            item: item to add
            location: location where to put the item
        """
        assert(not item == None)
        assert(not location == None)

        self.items.append(item)
        item.location = location
        item.level = self

    def get_items_at(self, location):
        """
        Get list of items at location

        Args:
            location: location to check
        """
        assert(location != None)
        items = []
        for item in self.items:
            if item.location == location:
                items.append(item)
        return items

    @Logged(__logger_name__)
    def add_portal(self, portal, location, other_end = None):
        """
        Adds precreated portal on level at given location
        If secondary portal is specified, link them together

        Args:
            portal: portal to add
            location: location where to add portal
            other_end: optional other end of the portal
        """
        assert(portal != None)
        assert(location != None)

        portal.level = self
        portal.location = location
        self.portals.append(portal)

        if other_end != None:
            assert(other_end.icon != None or portal.icon != None)

            portal.other_end = other_end
            other_end.other_end = portal

            if portal.icon != None:
                if other_end.icon == None:
                    if portal.icon == pyherc.data.tiles.PORTAL_STAIRS_DOWN:
                        other_end.icon = pyherc.data.tiles.PORTAL_STAIRS_UP
                    else:
                        other_end.icon = pyherc.data.tiles.PORTAL_STAIRS_DOWN
            else:
                if other_end.icon == pyherc.data.tiles.PORTAL_STAIRS_DOWN:
                    portal.icon = pyherc.data.tiles.PORTAL_STAIRS_UP
                else:
                    portal.icon = pyherc.data.tiles.PORTAL_STAIRS_DOWN

    def get_portal_at(self, location):
        """
        Check if there is a portal at given location

        Returns:
            Portal if found, otherwise None
        """
        for portal in self.portals:
            if portal.location == location:
                return portal

        return None

    @Logged(__logger_name__)
    def add_creature(self, creature, location = None):
        """
        Add a creature to level

        Args:
            creature: creature to add
            location: optional location for the creature
        """
        assert(creature != None)

        self.creatures.append(creature)
        creature.level = self
        if location != None:
            creature.location = location

    @Logged(__logger_name__)
    def remove_creature(self, creature):
        """
        Remove creature from level

        Args:
            creature: creature to remove
        """
        assert(creature != None)
        assert(creature in self.creatures)

        self.creatures.remove(creature)
        creature.level = None
        creature.location = ()

    def get_creature_at(self, location):
        """
        Get list of creatures at given location

        Args:
            location: location to check

        Returns:
            creature if found
        """
        assert(location != None)
        for creature in self.creatures:
            if creature.location == location:
                return creature

        return None

    @Logged(__logger_name__)
    def find_free_space(self):
        """
        Finds free space where stuff can be placed

        Returns:
            Location where space is free
        """
        width = len(self.floor)
        height = len(self.floor[0])
        location = (random.randint(2, width - 1), random.randint(2, height - 1))
        while self.walls[location[0]][location[1]] != pyherc.data.tiles.WALL_EMPTY:
            location = (random.randint(2, width - 1), random.randint(2, height - 1))
        return location

    def get_square(self, x_coordinate, y_coordinate):
        """
        Get square at given coordinates
        """
        if self.walls[x_coordinate][y_coordinate] != pyherc.data.tiles.WALL_EMPTY:
            return self.walls[x_coordinate][y_coordinate]
        else:
            return self.floor[x_coordinate][y_coordinate]

    def blocks_los(self, x_coordinate, y_coordinate):
        """
        Checks if there's LOS-blocking wall at given coordinates

        Args:
            x_coordinate: x-coordinate of the location
            y_coordinate: y-coordinate of the location

        Returns:
            True if location blocks line of sight, otherwise False
        """

        if self.walls[x_coordinate][y_coordinate] != pyherc.data.tiles.WALL_EMPTY:
            return False
        else:
            return True

    @Logged(__logger_name__)
    def get_size(self):
        """
        Gets size of level

        Returns:
            tupple, with width and length of level
        """
        x_size = len(self.floor)
        y_size = len(self.floor[0])

        return (x_size, y_size)

    @Logged(__logger_name__)
    def set_location_type(self, location, location_type):
        """
        Set type of location

        Args:
            location: (loc_x, loc_y) location to set
            location_type: type of location
        """
        self.__location_type[location[0]][location[1]] = location_type

    @Logged(__logger_name__)
    def get_location_type(self, location):
        """
        Get type of location

        Args:
            location: (loc_x, loc_y) location to get

        Returns:
            Type of location
        """
        return self.__location_type[location[0]][location[1]]

    @Logged(__logger_name__)
    def get_locations_by_type(self, location_type):
        """
        Get locations marked as rooms

        Args:
            location_type: Type of location to search.

        Returns:
            List of (loc_x, loc_y) locations identifying rooms
        """
        rooms = []
        for loc_x in range(len(self.__location_type)):
            for loc_y in range(len(self.__location_type[0])):
                if (self.__location_type[loc_x][loc_y] == location_type or
                        self.__location_type[loc_x][loc_y] != None
                        and location_type == 'any'):
                    rooms.append((loc_x, loc_y))

        return rooms

    def dump_string(self):
        """
        Dump this level into a string
        """
        level_string = ""
        size = self.get_size()
        for loc_y in range(size[1]):
            level_string = level_string + '\n'
            for loc_x in range(size[0]):
                creature = self.get_creature_at((loc_x, loc_y))
                portal = self.get_portal_at((loc_x, loc_y))
                items = self.get_items_at((loc_x, loc_y))

                if creature != None:
                    level_string = level_string + "X"
                elif portal != None:
                    level_string = level_string + "<"
                elif len(items) > 0:
                    level_string = level_string + "*"
                elif self.walls[loc_x][loc_y] != pyherc.data.tiles.WALL_EMPTY:
                    level_string = level_string + "#"
                elif self.walls[loc_x][loc_y] != pyherc.data.tiles.FLOOR_EMPTY:
                    level_string = level_string + "."
                else:
                    level_string = level_string + " "
        return level_string

class Dungeon(object):
    """
    Represents the dungeon
    """
    __logger_name__ = 'pyherc.data.dungeon.Dungeon'

    @Logged(__logger_name__)
    def __init__(self):
        super(Dungeon, self).__init__()
        self.levels = None
        self.logger = logging.getLogger('pyherc.data.dungeon.Dungeon')

    def __getstate__(self):
        """
        Override __getstate__ in order to get pickling work
        """
        properties = dict(self.__dict__)
        del properties['logger']
        return properties

    def __setstate__(self, properties):
        """
        Override __setstate__ in order to get pickling work
        """
        self.__dict__.update(properties)
        self.logger = logging.getLogger('pyherc.data.dungeon.Dungeon')

class Portal(object):
    """
    Portal linking two levels together
    """
    __logger_name__ = 'pyherc.data.dungeon.Portal'

    @Logged(__logger_name__)
    def __init__(self, icons, level_generator):
        """
        Default constructor

        Args:
            icons: (my_icon, icon for other end)
            level_generator: LevelGenerator for proxy portals
        """
        super(Portal, self).__init__()
        self.level = None
        self.location = ()
        self.__icons = icons
        self.__other_end = None
        self.level_generator = level_generator
        self.model = None
        self.logger = logging.getLogger('pyherc.data.dungeon.Portal')

    def __getstate__(self):
        """
        Override __getstate__ in order to get pickling work
        """
        properties = dict(self.__dict__)
        del properties['logger']
        return properties

    def __setstate__(self, properties):
        """
        Override __setstate__ in order to get pickling work
        """
        self.__dict__.update(properties)
        self.logger = logging.getLogger('pyherc.data.dungeon.Portal')

    @Logged(__logger_name__)
    def __get_other_end(self):
        """
        Returns the other end of the portal
        """
        if self.__other_end == None and self.level_generator != None:
            self.level_generator.generate_level(self)

        return self.__other_end

    @Logged(__logger_name__)
    def __set_other_end(self, portal):
        """
        Set the other end of the portal

        Args:
            portal: portal where this one leads
        """
        self.__other_end = portal

    def __get_icon(self):
        """
        Get icon to display this portal
        """
        return self.__icons[0]

    def __set_icon(self, icon):
        """
        Set icon to display this portal
        """
        if self.__icons == None:
            self.__icons = (None, None)
        self.__icons = (icon, self.__icons[1])

    def __get_other_end_icon(self):
        """
        Get icon used for other end of this portal
        """
        return self.__icons[1]

    other_end = property(__get_other_end, __set_other_end)
    icon = property(__get_icon, __set_icon)
    other_end_icon = property(__get_other_end_icon)
