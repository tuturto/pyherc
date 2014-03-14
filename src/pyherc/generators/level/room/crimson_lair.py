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
Classes for generating catacombs
"""
from pyherc.aspects import log_debug


class CrimsonLairGenerator():
    """
    Class for generating a catacomblike rooms
    """
    @log_debug
    def __init__(self, floor_tile, empty_tile, level_types, rng):
        """
        Default constructor

        :param floor_tile: id of the tile to use for floors
        :type floor_tile: integer
        :param empty_tile: id of the empty wall tile
        :type empty_tile: integer
        :param level_types: types of level this generator can be used
        :type level_types: [string]
        :param rng: random number generator
        :type rng: Random
        """
        super().__init__()
        self.floor_tile = floor_tile
        self.empty_tile = empty_tile
        self.room_width = None
        self.room_height = None
        self.level_types = level_types
        self.rng = rng

    @log_debug
    def generate_room(self, section):
        """
        Generate room

        :param section: section for generator to draw to
        :type section: Section
        """
        level_size = (section.width, section.height)
        for x_loc in range(1, level_size[0]):
            for y_loc in range(1, level_size[1]):
                section.set_floor((x_loc, y_loc),
                                  self.floor_tile,
                                  'room')
                section.set_wall((x_loc, y_loc),
                                 self.empty_tile,
                                 None)
