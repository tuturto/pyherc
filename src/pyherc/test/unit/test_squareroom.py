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
Tests for SquareRoomGenerator room generator
"""

from pyherc.data import Model, wall_tile
from pyherc.generators.level.partitioners import new_section, room_connections
from pyherc.generators.level.room import SquareRoomGenerator
from pyherc.test.builders import LevelBuilder
from hamcrest import assert_that, has_length, is_ 
import random

class TestSquareRoom():
    """
    Tests for SquareRoomGenerator room generator
    """
    def __init__(self):
        """
        Default constructor
        """
        self.level = None
        self.section = None
        self.generator = None
        self.floor_empty = 0
        self.floor_rock = 1
        self.wall_empty = 10
        self.wall_ground = 11
        self.rng = random.Random()

    def setup(self):
        """
        Setup the test case
        """
        self.level = (LevelBuilder()
                      .with_size((20, 20))
                      .with_floor_tile(self.floor_rock)
                      .with_wall_tile(self.wall_ground)
                      .build())

        self.section = new_section((5, 5), (15, 15), self.level, self.rng)
        self.generator = SquareRoomGenerator(self.floor_rock,
                                             self.wall_empty,
                                             self.floor_rock,
                                             ['crypt'])

    def test_generate_simple_room(self):
        """
        Test that generator can create a simple room
        """
        self.generator.generate_room(self.section)

        room_found = False
        for y_loc in range(20):
            for x_loc in range(20):
                if wall_tile(self.level, (x_loc, y_loc)) != self.wall_empty:
                    room_found = True

        assert_that(room_found, is_(True))

    def test_room_connections_are_placed(self):
        """
        Test that generating a square room will place 4 connectors
        """
        self.generator.generate_room(self.section)

        assert_that(list(room_connections(self.section)), has_length(4))
