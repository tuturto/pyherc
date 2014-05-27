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

import logging
from pyherc.data import floor_tile, wall_tile, add_trap, add_location_tag


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

        self.__corners = []
        self.__corners.append(corner1)
        self.__corners.append(corner2)
        self.level = level

        self.__connections = []
        self.__room_connections = []
        self.__neighbours = []
        self.random_generator = random_generator
        self.logger = logging.getLogger('pyherc.generators.level.partitioners.section.Section')  # noqa

    def __get_corners(self):
        """
        Get corners of this section

        :returns: corners of the section
        :rtype: [(integer, integer), (integer, integer)]
        """
        return self.__corners

    def __set_corners(self, corners):
        """
        Set corners of this section

        :param corners: Corners to set
        :type corners: [(integer, integer), (integer, integer)]
        """
        self.__corners = corners

    def __get_connections(self):
        """
        List of connections this section has

        :returns: connections of section
        :rtype: [Connection]
        """
        return self.__connections

    def __get_room_connections(self):
        """
        List of connections leading to the room

        :returns: connections
        :rtype: [Connection]
        """
        return self.__room_connections

    def __get_neighbours(self):
        """
        List of sections next to this one

        :returns: sections next to this one
        :rtype: [Section]
        """
        return self.__neighbours

    def __get_connected(self):
        """
        Is this section connected to a neighbour

        :returns: True if connected, otherwise False
        :rtype: Boolean
        """
        return len(self.__connections) > 0

    def __get_left_edge(self):
        """
        Get leftmost point of the section

        :returns: leftmost point of the section
        :rtype: (integer, integer)
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

        :returns: width of the section
        :rtype: integer
        """
        return abs(self.__corners[0][0] - self.__corners[1][0])

    def __get_top_edge(self):
        """
        Get top edge of the section

        :returns: highest point of the section
        :rtype: (integer, integer)
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

        :returns: height of the section
        :rtype: integer
        """
        return abs(self.__corners[0][1] - self.__corners[1][1])

    corners = property(__get_corners, __set_corners)
    """Corners of this Section."""

    connections = property(__get_connections)
    """Readonly property to access connections of the section"""

    room_connections = property(__get_room_connections)
    """Readonly property to access connections to the room"""

    neighbours = property(__get_neighbours)
    """Readonly property to access neighbours of the section"""

    connected = property(__get_connected)
    """Readonly property for connection status of the section

        :returns: True if section is connected, otherwise False
        :rtype: Boolean"""

    left_edge = property(__get_left_edge)
    """Readonly property to find leftmost point of the section"""

    width = property(__get_width)
    """Readonly property to calculate width of the section"""

    top_edge = property(__get_top_edge)
    """Readonly property to find topmost point of the section"""

    height = property(__get_height)
    """Readonly property to find height of the section"""

    def connect_to(self, section):
        """
        Connect this Section to another

        :param section: section to connect to
        :type section: Section
        """
        my_side_of_border = self.get_common_border(section)
        my_side = self.random_generator.choice(my_side_of_border)
        my_connection = Connection(connection=section,
                                   location=(my_side[0], my_side[1]),
                                   direction=my_side[2],
                                   section=self)
        self.connections.append(my_connection)

        other_side = section.get_opposing_point(my_side)
        other_connection = Connection(connection=self,
                                      location=(other_side[0],
                                                other_side[1]),
                                      direction=other_side[2],
                                      section=section)
        section.connections.append(other_connection)

    def unconnected_neighbours(self):
        """
        Get list of unconnected neighbours

        :returns: unconnected neighbours
        :rtype: [Section]
        """
        return [x for x in self.neighbours
                if not x.connected]

    def has_unconnected_neighbours(self):
        """
        Check if any of this Sections neighbours is unconnected

        :returns: True if unconnected neighbour is found, otherwise false
        :rtype: Boolean
        """
        return len(self.unconnected_neighbours()) > 0

    def get_border(self):
        """
        Get list of locations, defining borders of this Section

        :returns: List of (loc_x, loc_y, direction) defining borders
        :rtype: [(integer, integer, string)

        .. note:: coordinates are given relative to level origo
        """
        border = []

        assert len(self.__corners) == 2
        assert len(self.__corners[0]) == 2
        assert len(self.__corners[1]) == 2

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

        :returns: List of (loc_x, loc_y, direction) defining common border
        :rtype: [(integer, integer, string)]

        .. note:: Coordinates are given relative to level origo
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

        :param location: (loc_x, loc_y) defining point on the other side
        :type location: (integer, integer)
        :returns: (loc_x, loc_y) if corresponding point is found
        :rtype: (integer, integer) or Boolean

        .. note:: Coordinates are given relative to level origo
        .. note:: if not match is found, False is returned
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

        :param location: location where to add the Connection
        :type location: (integer, integer)
        :direction: direction where this connections leads
        :type direction: string

        .. note:: Coordinates are given relative to section origo
        """
        self.__room_connections.append(Connection(connection=None,
                                                  location=location,
                                                  direction=direction,
                                                  section=self))

    def set_floor(self, location, tile, location_type):
        """
        Set floor at given location

        :param location: location to set the tile
        :type location: (integer, integer)
        :param tile: ID of the tile to use
        :type tile: integer
        :param location_type: type of location, None to not change
        :type location_type: string

        .. note:: Coordinates are given relative to section origo
        """
        x_loc = self.__get_left_edge() + location[0]
        y_loc = self.__get_top_edge() + location[1]

        floor_tile(self.level, (x_loc, y_loc), tile)

        if location_type is not None:
            add_location_tag(self.level, (x_loc, y_loc), location_type)

    def get_floor(self, location):
        """
        Get floor tile in given location

        :param location: location to check
        :type location: (int, int)
        :returns: floor tile
        :rtype: int

        .. versionadded:: 0.8
        """
        x_loc = self.__get_left_edge() + location[0]
        y_loc = self.__get_top_edge() + location[1]

        return floor_tile(self.level, (x_loc, y_loc))

    def set_wall(self, location, tile, location_type):
        """
        Set wall at given location

        :param location: location to set the tile
        :type location: (integer, integer)
        :param tile: ID of the tile to use
        :type tile: integer
        :param location_type: type of location, None to not change
        :type location_type: string

        .. note:: Coordinates are given relative to section origo
        """
        x_loc = self.__get_left_edge() + location[0]
        y_loc = self.__get_top_edge() + location[1]

        wall_tile(self.level, (x_loc, y_loc), tile)
        if location_type is not None:
            add_location_tag(self.level, location, location_type)

    def set_location_type(self, location, location_type):
        """
        Set type of location in level

        :param location: location to set
        :type location: (int, int)
        :param location_type: type of location
        :type location_type: string

        .. versionadded:: 0.8
        """
        x_loc = self.__get_left_edge() + location[0]
        y_loc = self.__get_top_edge() + location[1]

        add_location_tag(self.level, (x_loc, y_loc), location_type)

    def get_wall(self, location):
        """
        Get wall at given location

        :param location: location to check
        :type location: (int, int)
        :returns: wall at given location
        :rtype: int

        .. versionadded:: 0.8
        """
        x_loc = self.__get_left_edge() + location[0]
        y_loc = self.__get_top_edge() + location[1]

        return wall_tile(self.level, (x_loc, y_loc))

    def find_room_connection(self, section_connection):
        """
        Find room connection that matches to given section connection

        :param section_connection: connection at the edge of section
        :type section_connection: Section
        :returns: matching room connection
        :rtype: Connection
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

    def add_trap(self, trap, location):
        """
        Add a trap to level

        :param trap: trap to add
        :type trap: Trap
        :param location: location to add the trap
        :type location: (int, int)

        .. versionadded:: 0.11

        .. note:: Coordinates are given relative to section origo
        """
        x_loc = self.__get_left_edge() + location[0]
        y_loc = self.__get_top_edge() + location[1]

        add_trap(self.level, (x_loc, y_loc), trap)


class Connection():
    """
    Connection between Sections or between Section and room
    """
    def __init__(self, connection, location, direction, section):
        """
        Default constructor

        :param connection: Connection on another Section,
                           if connecting between sections
        :type connection: Connection
        :param location: location of this connection
        :type location: (integer, integer)
        :param direction: direction where corridor should start from here
        :type direction: string
        :param section: section where connection is located
        :type section: Section
        """
        super().__init__()

        self.connection = connection
        self.location = location
        self.direction = direction
        self.section = section

    def translate_to_section(self):
        """
        Create a new Connection with coordinates translated to section

        :returns: new connection
        :rtype: Connection
        """
        new_location = (self.location[0] - self.section.left_edge,
                        self.location[1] - self.section.top_edge)

        new_connection = Connection(self.connection,
                                    new_location,
                                    self.direction,
                                    self.section)

        return new_connection
