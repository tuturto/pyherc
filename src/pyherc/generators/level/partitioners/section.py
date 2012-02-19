#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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

import random
import logging

class Section(object):
    """
    Class representing a single section in a level
    """
    def __init__(self, corner1, corner2, level):
        """
        Default constructor

        Args:
            corner1: Coordinates of first corner
            corner2: Coordinates of the second corner
            level: Level where Section is linked

        Note:
            Coordinates are given relative to level origo
        """
        self.__corners = []
        self.__corners.append(corner1)
        self.__corners.append(corner2)
        self.level = level

        self.__connections = []
        self.__room_connections = []
        self.__neighbours = []
        #TODO: inject from outside
        self.random_generator = random.Random()
        self.logger = logging.getLogger('pyherc.generators.level.partitioners.section.Section') #pylint: disable=C0301

    def __get_corners(self):
        """
        Get corners of this section
        """
        return self.__corners

    def __set_corners(self, corners):
        """
        Set corners of this section
        @param corners: corners to set
        """
        self.__corners = corners

    def __get_connections(self):
        """
        List of connections this section has
        """
        return self.__connections

    def __get_room_connections(self):
        """
        List of connections leading to the room
        """
        return self.__room_connections

    def __get_neighbours(self):
        """
        List of sections next to this one
        """
        return self.__neighbours

    def __get_connected(self):
        """
        Is this section connected to a neighbour

        Returns:
            True if connected, otherwise False
        """
        return len(self.__connections) > 0

    def __get_left_edge(self):
        """
        Get leftmost point of the section

        Returns:
            Leftmost point of the section
        """
        point1 = self.__corners[0][0]
        point2 = self.__corners[1][0]

        if point1 < point2:
            return point1
        else:
            return point2

    def __get_width(self):
        """
        Get width of the section

        Returns:
            Width of the section
        """
        return abs(self.__corners[0][0] - self.__corners[1][0])

    def __get_top_edge(self):
        """
        Get top edge of the section

        Returns:
            Highest point of the section
        """
        point1 = self.__corners[0][1]
        point2 = self.__corners[1][1]

        if point1 < point2:
            return point1
        else:
            return point2

    def __get_height(self):
        """
        Get height of the section

        Returns:
            Height of the section
        """
        return abs(self.__corners[0][1] - self.__corners[1][1])

    corners = property(__get_corners, __set_corners)
    """Corners of this Section.""" #pylint: disable=W0105

    connections = property(__get_connections)
    """Readonly property to access connections of the section""" #pylint: disable=W0105

    room_connections = property(__get_room_connections)
    """Readonly property to access connections to the room""" #pylint: disable=W0105

    neighbours = property(__get_neighbours)
    """Readonly property to access neighbours of the section""" #pylint: disable=W0105

    connected = property(__get_connected)
    """Readonly property for connection status of the section

        Returns:
            True if section is connected, otherwise False""" #pylint: disable=W0105

    left_edge = property(__get_left_edge)
    """Readonly property to find leftmost point of the section""" #pylint: disable=W0105

    width = property(__get_width)
    """Readonly property to calculate width of the section""" #pylint: disable=W0105

    top_edge = property(__get_top_edge)
    """Readonly property to find topmost point of the section""" #pylint: disable=W0105

    height = property(__get_height)
    """Readonly property to find height of the section""" #pylint: disable=W0105

    def connect_to(self, section):
        '''
        Connect this Section to another

        Args:
            section: Section to connect to
        '''
        my_side_of_border = self.get_common_border(section)
        my_side = self.random_generator.choice(my_side_of_border)
        my_connection = Connection(connection = section,
                                   location = (my_side[0], my_side[1]),
                                   direction = my_side[2],
                                   section = self)
        self.connections.append(my_connection)

        other_side = section.get_opposing_point(my_side)
        other_connection = Connection(connection = self,
                                   location = (other_side[0], other_side[1]),
                                   direction = other_side[2],
                                   section = section)
        section.connections.append(other_connection)

    def unconnected_neighbours(self):
        '''
        Get list of unconnected neighbours

        Returns:
            List of unconnected neighbours
        '''
        return [x for x in self.neighbours
                        if x.connected == False]

    def has_unconnected_neighbours(self):
        '''
        Check if any of this Sections neighbours is unconnected

        Returns:
            True if unconnected neighbour is found, otherwise false
        '''
        return len(self.unconnected_neighbours()) > 0

    def get_border(self):
        """
        Get list of locations, defining borders of this Section

        Returns:
            List of (loc_x, loc_y, direction) defining borders

        Note:
            Coordinates are given relative to level origo
        """
        border = []

        assert(len(self.__corners) == 2)
        assert(len(self.__corners[0]) == 2)
        assert(len(self.__corners[1]) == 2)

        for loc_x in range(self.__corners[0][0] + 1, self.__corners[1][0]):
            border.append((loc_x, self.__corners[0][1], "down"))
            border.append((loc_x, self.__corners[1][1], "up"))

        for loc_y in range(self.__corners[0][1] + 1, self.__corners[1][1]):
            border.append((self.__corners[0][0], loc_y, "right"))
            border.append((self.__corners[1][0], loc_y, "left"))

        return border

    def get_common_border(self, another_section):
        """
        Get list of locations that define common border between two Sections
        Border is placed on the edge of this Section

        Returns:
            List of (loc_x, loc_y, direection) defining common border

        Note:
            Coordinates are given relative to level origo
        """
        my_border = self.get_border()
        other_border = another_section.get_border()
        common_border = []

        for loc_1 in my_border:
            for loc_2 in other_border:
                if (loc_1[0] - loc_2[0])**2 + (loc_1[1] - loc_2[1])**2 == 1:
                    common_border.append(loc_1)

        return common_border

    def get_opposing_point(self, location):
        """
        Calculate which of this Section's points corresponds to the point given
        on the other side of the common border

        Args:
            location: (loc_x, loc_y) defining point on the other side

        Returns:
            (loc_x, loc_y) if corresponding point is found, False otherwise

        Note:
            Coordinates are given relative to level origo
        """
        my_side = None
        my_border = self.get_border()

        for loc_1 in my_border:
            if (loc_1[0] - location[0])**2 + (loc_1[1] - location[1])**2 == 1:
                my_side = loc_1

        return my_side

    def add_room_connection(self, location, direction):
        """
        Adds connection to the room

        Room connections are used to connect rooms to edge of Sections

        Args:
            location: (loc_x, loc_y) where to add the Connection
            direction: direction where this connections leads

        Note:
            Coordinates are given relative to section origo
        """
        self.__room_connections.append(
                        Connection(connection = None,
                                   location = location,
                                   direction = direction,
                                   section = self))

    def set_floor(self, location, tile):
        """
        Set floor at given location

        Args:
            location: (loc_x, loc_y) location to set the tile
            tile: ID of the tile to use

        Note:
            Coordinates are given relative to section origo
        """
        x_loc = self.__get_left_edge() + location[0]
        y_loc = self.__get_top_edge() + location[1]

        self.level.floor[x_loc][y_loc] = tile

    def set_wall(self, location, tile):
        """
        Set wall at given location

        Args:
            location: (loc_x, loc_y) location to set the tile
            tile: ID of the tile to use

        Note:
            Coordinates are given relative to section origo
        """
        x_loc = self.__get_left_edge() + location[0]
        y_loc = self.__get_top_edge() + location[1]

        self.level.walls[x_loc][y_loc] = tile

    def find_room_connection(self, section_connection):
        """
        Find room connection that matches to given section connection

        Args:
            section_connection: Connection at the edge of section

        Returns:
            matching room Connection
        """
        wanted = None
        if section_connection.direction == "left":
            wanted = "right"
        elif section_connection.direction == "right":
            wanted = "left"
        elif section_connection.direction == "up":
            wanted = "down"
        else:
            wanted = "up"

        possible_connections = [x for x in self.room_connections
                                if x.direction == wanted]

        connection = self.random_generator.choice(possible_connections)

        return connection

class Connection(object):
    """
    Connection between Sections or between Section and room
    """
    def __init__(self, connection, location, direction, section):
        """
        Default constructor

        Args:
            connection: Connection on another Section,
                    if connecting between sections
            location: (x_loc, y_loc) of this connection
            direction: direction where corridor should start from here
            section: Section where connection is located
        """
        object.__init__(self)
        self.connection = connection
        self.location = location
        self.direction = direction
        self.section = section

    def translate_to_section(self):
        """
        Create a new Connection with coordinates translated to section

        Returns:
            New connection
        """
        new_location = (self.location[0] - self.section.left_edge,
                        self.location[1] - self.section.top_edge)

        new_connection = Connection(self.connection,
                                    new_location,
                                    self.direction,
                                    self.section)

        return new_connection

