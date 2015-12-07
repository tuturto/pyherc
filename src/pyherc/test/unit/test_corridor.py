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
Tests for Corridor
"""

import random

from hamcrest import assert_that, equal_to, is_

from pyherc.data import tile, wall_tile, floor_tile
from pyherc.generators.level.partitioners import (section_connections,
                                                  add_room_connection,
                                                  add_section_connection)
from pyherc.generators.level.partitioners import Connection, new_section
from pyherc.generators.level.room.corridor import CorridorGenerator
from pyherc.test.matchers import is_fully_accessible
from pyherc.test.builders import LevelBuilder


class TestCorridor():
    """
    Tests for Corridor
    """
    def __init__(self):
        """
        Default constructor
        """
        self.level = None
        self.section = None
        self.rng = None
        self.floor_rock = None
        self.wall_ground = None

    def setup(self):
        """
        Setup the test case
        """
        self.floor_rock = 1
        self.wall_ground = 2

        self.level = (LevelBuilder()
                        .with_size((10, 10))
                        .with_floor_tile(self.floor_rock)
                        .with_wall_tile(self.wall_ground)
                        .build())

        self.rng = random.Random()
        self.section = new_section((0, 0),
                                   (10, 10),
                                   self.level,
                                   self.rng)

    def test_straight_horizontal(self):
        """
        Test that straight horizontal corridor can be made
        """
        edge_connection = Connection(connection=None,
                                     location=(10, 5),
                                     direction="left",
                                     section=self.section)

        room_connection = Connection(connection=None,
                                     location=(5, 5),
                                     direction="right",
                                     section=self.section)

        add_section_connection(self.section, edge_connection)
        add_room_connection(self.section, (5, 5), "right")

        generator = CorridorGenerator(start_point=edge_connection,
                                      end_point=room_connection,
                                      wall_tile=None,
                                      floor_tile=self.floor_rock)

        generator.generate()

        for x_loc in range(5, 11):
            assert_that(floor_tile(self.level, (x_loc, 5)),
                        is_(equal_to(self.floor_rock)))

    def test_straight_vertical(self):
        """
        Test that straight vertical corridor can be made
        """
        edge_connection = Connection(connection=None,
                                     location=(5, 0),
                                     direction="down",
                                     section=self.section)

        room_connection = Connection(connection=None,
                                     location=(5, 5),
                                     direction="up",
                                     section=self.section)

        add_section_connection(self.section, edge_connection)
        add_room_connection(self.section, (5, 5), "up")

        generator = CorridorGenerator(start_point=edge_connection,
                                      end_point=room_connection,
                                      wall_tile=None,
                                      floor_tile=self.floor_rock)

        generator.generate()

        for y_loc in range(0, 6):
            assert_that(floor_tile(self.level, (5, y_loc)),
                        is_(equal_to(self.floor_rock)))

    def test_bent_horizontal(self):
        """
        Test that horizontal corridor with bend can be made
        """
        edge_connection = Connection(connection=None,
                                     location=(10, 2),
                                     direction="left",
                                     section=self.section)

        room_connection = Connection(connection=None,
                                     location=(5, 8),
                                     direction="right",
                                     section=self.section)

        add_section_connection(self.section, edge_connection)
        add_room_connection(self.section, (5, 8), "right")

        generator = CorridorGenerator(start_point=edge_connection,
                                      end_point=room_connection,
                                      wall_tile=None,
                                      floor_tile=self.floor_rock)

        generator.generate()

        assert_that(wall_tile(self.level, (10, 2)),
                    is_(equal_to(None)))
        assert_that(wall_tile(self.level, (5, 8)),
                    is_(equal_to(None)))
        assert_that(self.level, is_fully_accessible())

    def test_bent_vertical(self):
        """
        Test that horizontal corridor with bend can be made
        """
        edge_connection = Connection(connection=None,
                                     location=(9, 0),
                                     direction="down",
                                     section=self.section)

        room_connection = Connection(connection=None,
                                     location=(2, 9),
                                     direction="up",
                                     section=self.section)

        add_section_connection(self.section, edge_connection)
        add_room_connection(self.section, (2, 9), "up")

        generator = CorridorGenerator(start_point=edge_connection,
                                      end_point=room_connection,
                                      wall_tile=None,
                                      floor_tile=self.floor_rock)

        generator.generate()

        assert_that(wall_tile(self.level, (9, 0)),
                    is_(equal_to(None)))
        assert_that(wall_tile(self.level, (2, 9)),
                    is_(equal_to(None)))
        assert_that(self.level, is_fully_accessible())
