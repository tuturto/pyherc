# -*- coding: utf-8 -*-

# Copyright (c) 2010-2017 Tuukka Turto
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
Classes for generating catacombs
"""
from pyherc.aspects import log_debug
from pyherc.generators.level.partitioners import (section_width, section_height,
                                                  section_floor, section_wall)

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
        level_size = (section_width(section), section_height(section))
        for x_loc in range(1, level_size[0]):
            for y_loc in range(1, level_size[1]):
                section_floor(section,
                              (x_loc, y_loc),
                              self.floor_tile,
                              'room')
                section_wall(section,
                             (x_loc, y_loc),
                             self.empty_tile,
                             None)
