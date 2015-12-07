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
Classes for generating pillar rooms
"""

from random import Random

from pyherc.aspects import log_debug
from pyherc.generators.level.room.squareroom import SquareRoomGenerator
from pyherc.generators.level.partitioners import section_floor, section_wall


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

    def __call__(self, section):
        """
        Generate room
        """
        self.generate_room(section)

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

        if section_wall(section, location) == self.empty_tile:
            section_wall(section,
                         location,
                         self.pillar_tile,
                         None)
            section_floor(section,
                          location,
                          None,
                          None)
