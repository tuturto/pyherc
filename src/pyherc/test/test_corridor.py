#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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
#pylint: disable=W0614
from pyDoubles.framework import spy #pylint: disable=F0401, E0611
from pyDoubles.framework import assert_that_method #pylint: disable=F0401, E0611
from hamcrest import * #pylint: disable=W0401

from pyherc.data import Level
from pyherc.generators.level.partitioners.section import Section, Connection
from pyherc.generators.level.room.corridor import CorridorGenerator
from pyherc.data.tiles import FLOOR_ROCK
from pyherc.data.tiles import WALL_GROUND
from pyherc.data.tiles import WALL_EMPTY

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

    def setup(self):
        """
        Setup the test case
        """
        self.level = Level(size = (10, 10),
                      floor_type = FLOOR_ROCK,
                      wall_type = WALL_GROUND)

        self.section = Section(corner1 = (0, 0),
                          corner2 = (10, 10),
                          level = self.level)

    def test_straight_horizontal(self):
        """
        Test that straight horizontal corridor can be made
        """
        edge_connection = Connection(connection = None,
                                     location = (10, 5),
                                     direction = "left",
                                     section = self.section)

        room_connection = Connection(connection = None,
                                     location = (5, 5),
                                     direction = "right",
                                     section = self.section)

        self.section.connections.append(edge_connection)
        self.section.room_connections.append(room_connection)

        generator = CorridorGenerator(start_point = edge_connection,
                                      end_point = room_connection,
                                      tile = WALL_EMPTY)

        generator.generate()

        for x_loc in range(5, 11):
            assert_that(self.level.get_tile(x_loc, 5), is_(equal_to(FLOOR_ROCK)))

    def test_straight_vertical(self):
        """
        Test that straight vertical corridor can be made
        """
        edge_connection = Connection(connection = None,
                                     location = (5, 0),
                                     direction = "down",
                                     section = self.section)

        room_connection = Connection(connection = None,
                                     location = (5, 5),
                                     direction = "up",
                                     section = self.section)

        self.section.connections.append(edge_connection)
        self.section.room_connections.append(room_connection)

        generator = CorridorGenerator(start_point = edge_connection,
                                      end_point = room_connection,
                                      tile = WALL_EMPTY)

        generator.generate()

        for y_loc in range(0, 6):
            assert_that(self.level.get_tile(5, y_loc), is_(equal_to(FLOOR_ROCK)))
