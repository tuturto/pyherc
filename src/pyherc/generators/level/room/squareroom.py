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
Classes for generating square rooms
"""

import logging
from random import Random

from pyherc.generators.level.room.corridor import CorridorGenerator
from pyherc.generators.level.partitioners import (section_width,
                                                  section_height,
                                                  section_floor, section_wall,
                                                  section_connections,
                                                  add_room_connection,
                                                  match_section_to_room)


class SquareRoomGenerator():
    """
    Class for generating a square room
    """
    def __init__(self, floor_tile, empty_tile, corridor_tile, level_types):
        """
        Default constructor

        :param floor_tile: id of the tile to use for floors
        :type floor_tile: integer
        :param empty_tile: id of the empty wall tile
        :type empty_tile: integer
        :param corridor_tile: id of corridor floor tile
        :type corridor_tile: integer
        :param level_types: types of level this generator can be used
        :type level_types: [string]
        """
        self.floor_tile = floor_tile
        self.corridor_tile = corridor_tile
        self.empty_tile = empty_tile
        self.room_width = None
        self.room_height = None
        self.level_types = level_types
        self.rng = Random()
        self.room_corners = []
        self.rows = []
        self.logger = logging.getLogger('pyherc.generators.level.room.squareroom.SquareRoomGenerator')  # noqa

    def __call__(self, section):
        """
        Generate room
        """
        self.generate_room(section)

    def generate_room(self, section):
        """
        Generate room

        :param section: section for generator to draw to
        :type section: Section
        """

        middle_height = section_height(section) // 2
        middle_width = section_width(section) // 2

        if len([x for x in section_connections(section)
                if x.direction == 'right']) > 0:
            room_left_edge = self.rng.randint(2, middle_width - 2)
        else:
            room_left_edge = 1

        if len([x for x in section_connections(section)
                if x.direction == 'left']) > 0:
            room_right_edge = self.rng.randint(middle_width + 2,
                                               section_width(section) - 2)
        else:
            room_right_edge = section_width(section) - 1

        if len([x for x in section_connections(section)
                if x.direction == 'down']) > 0:
            room_top_edge = self.rng.randint(2, middle_height - 2)
        else:
            room_top_edge = 1

        if len([x for x in section_connections(section)
                if x.direction == 'up']) > 0:
            room_bottom_edge = self.rng.randint(middle_height + 2,
                                                section_height(section) - 2)
        else:
            room_bottom_edge = section_height(section) - 1

        for loc_y in range(room_top_edge + 1, room_bottom_edge):
            for loc_x in range(room_left_edge + 1, room_right_edge):
                section_floor(section, (loc_x, loc_y), self.floor_tile, 'room')
                section_wall(section, (loc_x, loc_y), self.empty_tile, None)

        center_x = (room_right_edge - room_left_edge) // 2 + room_left_edge
        center_y = (room_bottom_edge - room_top_edge) // 2 + room_top_edge

        add_room_connection(section, (center_x, room_top_edge), "up")
        add_room_connection(section, (center_x, room_bottom_edge), "down")
        add_room_connection(section, (room_left_edge, center_y), "left")
        add_room_connection(section, (room_right_edge, center_y), "right")

        self.add_corridors(section)

        self.room_corners = []
        self.room_corners.append((room_left_edge + 1, room_top_edge + 1))
        self.room_corners.append((room_right_edge - 1, room_top_edge + 1))
        self.room_corners.append((room_right_edge - 1, room_bottom_edge - 1))
        self.room_corners.append((room_left_edge + 1, room_bottom_edge - 1))

        self.add_rows()

    def add_rows(self):
        """
        Add extra info detailing rows that can be used for bookshelves and such
        """
        self.rows = []

        top_left = self.room_corners[0]
        top_right = self.room_corners[1]
        bottom_right = self.room_corners[2]
        bottom_left = self.room_corners[3]

        rows = range(top_left[1] + 1, bottom_left[1], 2)
        cols = range(top_left[0] + 1, top_right[0])

        for y in rows:
            for x in cols:
                self.rows.append((x, y))

    def add_corridors(self, section):
        """
        Add corridors leading from room connection to section connections

        :param section: section to add corridors
        :type section: Section
        """
        for section_connection in section_connections(section):
            room_connection = match_section_to_room(section,
                                                    section_connection)
            corridor = CorridorGenerator(
                room_connection,
                section_connection.translate_to_section(),
                self.empty_tile,
                self.corridor_tile)
            corridor.generate()
