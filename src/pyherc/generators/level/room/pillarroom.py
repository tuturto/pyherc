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
Classes for generating pillar rooms
"""

from random import Random

from pyherc.aspects import log_debug
from pyherc.generators.level.room.squareroom import SquareRoomGenerator


class PillarRoomGenerator():
    """
    Class for generating a pillar room

    .. versionadded:: 0.8
    """
    @log_debug
    def __init__(self, floor_tile, corridor_tile, empty_tile, pillar_tile,
                 level_types):
        """
        Default constructor

        :param floor_tile: id of the tile to use for floors
        :type floor_tile: integer
        :param corridor_tile: id of the tile to use for corridor floors
        :type corridor_tile: integer
        :param empty_tile: id of the empty wall tile
        :type empty_tile: integer
        :param level_types: types of level this generator can be used
        :type level_types: [string]
        """
        self.square_generator = SquareRoomGenerator(floor_tile,
                                                    empty_tile,
                                                    corridor_tile,
                                                    level_types)
        self.floor_tile = floor_tile
        self.corridor_tile = corridor_tile
        self.empty_tile = empty_tile
        self.level_types = level_types
        self.pillar_tile = pillar_tile
        self.rng = Random()

    @log_debug
    def generate_room(self, section):
        """
        Generate room

        :param section: section for generator to draw to
        :type section: Section
        """
        self.square_generator.generate_room(section)

        offset = [(1, 1), (-1, 1), (-1, -1), (1, -1)]

        for index, corner in enumerate(self.square_generator.room_corners):
            self.add_pillar(section, corner, offset[index])

    @log_debug
    def add_pillar(self, section, corner, pillar):
        """
        Add pillar if location is free
        """
        location = (corner[0] + pillar[0],
                    corner[1] + pillar[1])

        if section.get_wall(location) == self.empty_tile:
            section.set_wall(location=location,
                             tile=self.pillar_tile,
                             location_type=None)
            section.set_floor(location=location,
                              tile=None,
                              location_type=None)
