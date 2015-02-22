# -*- coding: utf-8 -*-

#   Copyright 2010-2015 Tuukka Turto
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
