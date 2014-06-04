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
from pyherc.data import get_tile, ornamentation
from pyherc.generators.level.partitioners.new_section import (section_to_map,
                                                              left_edge,
                                                              top_edge,
                                                              is_connected)

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

        self._corners = []
        self._corners.append(corner1)
        self._corners.append(corner2)
        self.level = level

        self._connections = []
        self._room_connections = []
        self._neighbours = []
        self.random_generator = random_generator
        self.logger = logging.getLogger('pyherc.generators.level.partitioners.section.Section')  # noqa

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
        self._connections.append(my_connection)

        other_side = section.get_opposing_point(my_side)
        other_connection = Connection(connection=self,
                                      location=(other_side[0],
                                                other_side[1]),
                                      direction=other_side[2],
                                      section=section)
        section._connections.append(other_connection)

    def get_border(self):
        """
        Get list of locations, defining borders of this Section

        :returns: List of (loc_x, loc_y, direction) defining borders
        :rtype: [(integer, integer, string)

        .. note:: coordinates are given relative to level origo
        """
        border = []

        assert len(self._corners) == 2
        assert len(self._corners[0]) == 2
        assert len(self._corners[1]) == 2

        for loc_x in range(self._corners[0][0] + 1, self._corners[1][0]):
            border.append((loc_x, self._corners[0][1], "down"))
            border.append((loc_x, self._corners[1][1], "up"))

        for loc_y in range(self._corners[0][1] + 1, self._corners[1][1]):
            border.append((self._corners[0][0], loc_y, "right"))
            border.append((self._corners[1][0], loc_y, "left"))

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
        self._room_connections.append(Connection(connection=None,
                                                 location=location,
                                                 direction=direction,
                                                 section=self))

    def set_location_type(self, location, location_type):
        """
        Set type of location in level

        :param location: location to set
        :type location: (int, int)
        :param location_type: type of location
        :type location_type: string

        .. versionadded:: 0.8
        """
        add_location_tag(self.level, section_to_map(self, location), location_type)

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

        possible_connections = [x for x in self._room_connections
                                if x.direction == wanted]

        connection = self.random_generator.choice(possible_connections)

        return connection

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
        new_location = (self.location[0] - left_edge(self.section),
                        self.location[1] - top_edge(self.section))

        new_connection = Connection(self.connection,
                                    new_location,
                                    self.direction,
                                    self.section)

        return new_connection
