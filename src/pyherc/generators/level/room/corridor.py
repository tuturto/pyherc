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
Classes for generating corridors
"""

from pyherc.generators.level.partitioners import (Connection, section_floor,
                                                  section_wall, section_connections,
                                                  match_section_to_room)

def corridors(floor_tile):
    "create corridors"

    def corridor(section, trap_generator=None):
        "carve corridors"
        for it in section_connections(section):
            room_connection = match_section_to_room(section, it)
            corridor = CorridorGenerator(room_connection,
                                         it.translate_to_section(),
                                         None,
                                         floor_tile)
            corridor.generate()

    return corridor

class CorridorGenerator():
    """
    Class for making simple corridors
    """
    def __init__(self, start_point, end_point, wall_tile, floor_tile):
        """
        Default constructor

        :param start_point: starting connection
        :type start_point: Connection
        :param end_point: ending connection
        :type end_point: Connection
        :param wall_tile: ID of wall tile to place
        :type wall_tile: integer
        :param floor_tile: ID of floor tile to place
        :type floor_tile: integer
        """
        self.start_point = start_point
        self.end_point = end_point
        self.wall_tile = wall_tile
        self.floor_tile = floor_tile

    def generate(self):
        """
        Carves corridor from start_point to end_point
        """
        if self.start_point.location[1] == self.end_point.location[1]:
            self.__carve_horizontal(self.start_point, self.end_point)
        elif self.start_point.location[0] == self.end_point.location[0]:
            self.__carve_vertical(self.start_point, self.end_point)
        elif self.start_point.direction in ("left", "right"):
            self.__carve_horizontal_bend(self.start_point, self.end_point)
        elif self.start_point.direction in ("up", "down"):
            self.__carve_vertical_bend(self.start_point, self.end_point)

    def __carve_horizontal(self, start_point, end_point):
        """
        Special case, carving is done in straigth horizontal line

        :param start_point: starting connection
        :type start_point: Connection
        :param end_point: ending connection
        :type end_point: Connection
        """
        if start_point.location[0] > end_point.location[0]:
            start_x = end_point.location[0]
            end_x = start_point.location[0]
        else:
            start_x = start_point.location[0]
            end_x = end_point.location[0]

        y_loc = start_point.location[1]
        section = start_point.section

        for x_loc in range(start_x, end_x):
            section_wall(section, (x_loc, y_loc), self.wall_tile, 'corridor')
            section_floor(section, (x_loc, y_loc), self.floor_tile, None)

        section_wall(section, end_point.location, self.wall_tile, 'corridor')
        section_wall(section, start_point.location, self.wall_tile, 'corridor')
        section_floor(section, end_point.location, self.floor_tile, None)
        section_floor(section, start_point.location, self.floor_tile, None)

    def __carve_horizontal_bend(self, start_point, end_point):
        """
        Carve corridor in three sections (horizontal, vertical, horizontal)

        :param start_point: starting connection
        :type start_point: Connection
        :param end_point: ending connection
        :type end_point: Connection
        """
        middle_x = abs(start_point.location[0] - end_point.location[0]) // 2

        if start_point.location[0] < end_point.location[0]:
            middle_x = middle_x + start_point.location[0]
        else:
            middle_x = middle_x + end_point.location[0]

        middle_start = Connection(None,
                                  (middle_x, start_point.location[1]),
                                  None,
                                  self.start_point.section)

        middle_end = Connection(None,
                                (middle_x, end_point.location[1]),
                                None,
                                self.start_point.section)

        self.__carve_horizontal(start_point, middle_start)
        self.__carve_vertical(middle_start, middle_end)
        self.__carve_horizontal(middle_end, end_point)

    def __carve_vertical(self, start_point, end_point):
        """
        Special case, carving is done in straigth vertical line

        :param start_point: starting connection
        :type start_point: Connection
        :param end_point: ending connection
        :type end_point: Connection
        """
        if start_point.location[1] > end_point.location[1]:
            start_y = end_point.location[1]
            end_y = start_point.location[1]
        else:
            start_y = start_point.location[1]
            end_y = end_point.location[1]

        x_loc = start_point.location[0]
        section = start_point.section

        for y_loc in range(start_y, end_y):
            section_wall(section, (x_loc, y_loc), self.wall_tile, 'corridor')
            section_floor(section, (x_loc, y_loc), self.floor_tile, None)

        section_wall(section, end_point.location, self.wall_tile, 'corridor')
        section_wall(section, start_point.location, self.wall_tile, 'corridor')
        section_floor(section, end_point.location, self.floor_tile, None)
        section_floor(section, start_point.location, self.floor_tile, None)

    def __carve_vertical_bend(self, start_point, end_point):
        """
        Carve corridor in three sections (vertical, horizontal,vertical)

        :param start_point: starting connection
        :type start_point: Connection
        :param end_point: ending connection
        :type end_point: Connection
        """
        middle_y = abs(start_point.location[1] - end_point.location[1]) // 2

        if start_point.location[1] < end_point.location[1]:
            middle_y = middle_y + start_point.location[1]
        else:
            middle_y = middle_y + end_point.location[1]

        middle_start = Connection(None,
                                  (start_point.location[0], middle_y),
                                  None,
                                  self.start_point.section)

        middle_end = Connection(None,
                                (end_point.location[0], middle_y),
                                None,
                                self.start_point.section)

        self.__carve_vertical(start_point, middle_start)
        self.__carve_horizontal(middle_start, middle_end)
        self.__carve_vertical(middle_end, end_point)
