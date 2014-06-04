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
                                                              is_connected,
                                                              section_border,
                                                              common_border,
                                                              opposing_point,
                                                              Connection)

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
        my_side_of_border = list(common_border(self, section))
        my_side = self.random_generator.choice(my_side_of_border)
        my_connection = Connection(connection=section,
                                   location=(my_side[0], my_side[1]),
                                   direction=my_side[2],
                                   section=self)
        self._connections.append(my_connection)

        other_side = opposing_point(section, my_side)
        other_connection = Connection(connection=self,
                                      location=(other_side[0],
                                                other_side[1]),
                                      direction=other_side[2],
                                      section=section)
        section._connections.append(other_connection)

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
