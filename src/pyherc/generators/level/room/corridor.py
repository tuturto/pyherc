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
Classes for generating corridors
"""

from pyherc.generators.level.partitioners.section import Connection


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
            section.set_wall((x_loc, y_loc), self.wall_tile, 'corridor')
            section.set_floor((x_loc, y_loc), self.floor_tile, None)

        section.set_wall(end_point.location, self.wall_tile, 'corridor')
        section.set_wall(start_point.location, self.wall_tile, 'corridor')
        section.set_floor(end_point.location, self.floor_tile, None)
        section.set_floor(start_point.location, self.floor_tile, None)

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
            section.set_wall((x_loc, y_loc), self.wall_tile, 'corridor')
            section.set_floor((x_loc, y_loc), self.floor_tile, None)

        section.set_wall(end_point.location, self.wall_tile, 'corridor')
        section.set_wall(start_point.location, self.wall_tile, 'corridor')
        section.set_floor(end_point.location, self.floor_tile, None)
        section.set_floor(start_point.location, self.floor_tile, None)

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
