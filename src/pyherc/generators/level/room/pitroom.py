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
Classes for generating pit rooms
"""

from pyherc.aspects import log_debug
from pyherc.generators.level.room.squareroom import SquareRoomGenerator


class PitRoomGenerator():
    """
    Class for generating a room with pit

    .. versionadded:: 0.11
    """
    @log_debug
    def __init__(self, floor_tile, corridor_tile, empty_tile, pit_tile,
                 trap_type, level_types):
        """
        Default constructor

        :param floor_tile: id of the tile to use for floors
        :type floor_tile: icon key
        :param corridor_tile: id of the tile to use for corridor floors
        :type corridor_tile: icon key
        :param empty_tile: id of the empty wall tile
        :type empty_tile: icon key
        :param pit_tile: id of the pit tile
        :type pit_tile: icon key
        :param trap_type: type of trap to use
        :type trap_type: Type
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
        self.pit_tile = pit_tile
        self.trap_type = trap_type

    @log_debug
    def generate_room(self, section):
        """
        Generate room

        :param section: section for generator to draw to
        :type section: Section
        """
        self.square_generator.generate_room(section)

        top_left = self.square_generator.room_corners[0]
        bottom_right = self.square_generator.room_corners[2]

        for loc_x in range(top_left[0]+1, bottom_right[0]):
            for loc_y in range(top_left[1]+1, bottom_right[1]):
                section.set_floor(location=(loc_x, loc_y),
                                  tile=self.pit_tile,
                                  location_type='pit')
                section.add_trap(self.trap_type(),
                                 (loc_x, loc_y))
