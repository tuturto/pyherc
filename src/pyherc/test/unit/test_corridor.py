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
Tests for Corridor
"""

import random

from hamcrest import assert_that, equal_to, is_
from pyherc.data import Level
from pyherc.generators.level.partitioners.section import Connection, Section
from pyherc.generators.level.room.corridor import CorridorGenerator
from pyherc.test.matchers import is_fully_accessible_via


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
        self.wall_empty = None

    def setup(self):
        """
        Setup the test case
        """
        self.floor_rock = 1
        self.wall_ground = 2
        self.wall_empty = 3

        self.level = Level(size=(10, 10),
                           floor_type=self.floor_rock,
                           wall_type=self.wall_ground,
                           empty_wall=self.wall_empty)

        self.rng = random.Random()
        self.section = Section(corner1=(0, 0),
                               corner2=(10, 10),
                               level=self.level,
                               random_generator=self.rng)

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

        self.section.connections.append(edge_connection)
        self.section.room_connections.append(room_connection)

        generator = CorridorGenerator(start_point=edge_connection,
                                      end_point=room_connection,
                                      wall_tile=self.wall_empty,
                                      floor_tile=self.floor_rock)

        generator.generate()

        for x_loc in range(5, 11):
            assert_that(self.level.get_tile(x_loc, 5),
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

        self.section.connections.append(edge_connection)
        self.section.room_connections.append(room_connection)

        generator = CorridorGenerator(start_point=edge_connection,
                                      end_point=room_connection,
                                      wall_tile=self.wall_empty,
                                      floor_tile=self.floor_rock)

        generator.generate()

        for y_loc in range(0, 6):
            assert_that(self.level.get_tile(5, y_loc),
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

        self.section.connections.append(edge_connection)
        self.section.room_connections.append(room_connection)

        generator = CorridorGenerator(start_point=edge_connection,
                                      end_point=room_connection,
                                      wall_tile=self.wall_empty,
                                      floor_tile=self.floor_rock)

        generator.generate()

        assert_that(self.level.get_wall_tile(10, 2),
                    is_(equal_to(self.wall_empty)))
        assert_that(self.level.get_wall_tile(5, 8),
                    is_(equal_to(self.wall_empty)))
        assert_that(self.level, is_fully_accessible_via(self.wall_empty))

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

        self.section.connections.append(edge_connection)
        self.section.room_connections.append(room_connection)

        generator = CorridorGenerator(start_point=edge_connection,
                                      end_point=room_connection,
                                      wall_tile=self.wall_empty,
                                      floor_tile=self.floor_rock)

        generator.generate()

        assert_that(self.level.get_wall_tile(9, 0),
                    is_(equal_to(self.wall_empty)))
        assert_that(self.level.get_wall_tile(2, 9),
                    is_(equal_to(self.wall_empty)))
        assert_that(self.level, is_fully_accessible_via(self.wall_empty))
