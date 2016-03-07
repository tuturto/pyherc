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
tests for path finding
"""
from random import Random

from hamcrest import assert_that, contains, is_
from mockito import mock
from pyherc.ai import a_star
from pyherc.config.dsl import LevelContext
from pyherc.data import Portal, Model, find_free_space, wall_tile
from pyherc.data.geometry import free_locations_around
from pyherc.generators.level.partitioners import grid_partitioning
from pyherc.generators.level.portal import PortalAdder
from pyherc.generators.level.room.catacombs import CatacombsGenerator
from pyherc.test.builders import LevelBuilder
from pyherc.test.matchers import continuous_path

FLOOR_TILE = 100
WALL_TILE = 200
EMPTY_TILE = None

class TestAStar():
    """
    Tests for A* path finding
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def test_simple_path(self):
        """
        Test that a simple path can be found
        """
        level = (LevelBuilder()
                    .with_floor_tile(FLOOR_TILE)
                    .with_wall_tile(EMPTY_TILE)
                    .with_solid_wall_tile(WALL_TILE)
                    .build())

        path, connections, updated = a_star(start = (1, 1),
                                            goal = (5, 1),
                                            a_map = level,
                                            adjacent_nodes = free_locations_around)

        assert_that(path, contains((1, 1),
                                   (2, 1),
                                   (3, 1),
                                   (4, 1),
                                   (5, 1)))

    def test_going_around_wall(self):
        """
        Test that path can be found around a wall
        """
        level = (LevelBuilder()
                    .with_floor_tile(FLOOR_TILE)
                    .with_wall_tile(EMPTY_TILE)
                    .with_solid_wall_tile(WALL_TILE)
                    .with_wall_at((12, 8))
                    .with_wall_at((12, 9))
                    .with_wall_at((12, 10))
                    .with_wall_at((12, 11))
                    .with_wall_at((12, 12))
                    .with_size((20, 20))
                    .build())

        path, connections, updated = a_star(start = (10, 10),
                                            goal = (15, 10),
                                            a_map = level,
                                            adjacent_nodes = free_locations_around)

        assert_that(path, is_(continuous_path(start = (10, 10),
                                              destination = (15, 10),
                                              level = level)))
