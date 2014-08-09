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
tests for path finding
"""
from random import Random

from hamcrest import assert_that, contains, is_
from mockito import mock
from pyherc.ai import a_star
from pyherc.config.dsl import LevelContext
from pyherc.data import Portal, Model, find_free_space, wall_tile
from pyherc.generators.level.generator import LevelGenerator
from pyherc.generators.level.partitioners import GridPartitioner
from pyherc.generators.level.portals import PortalAdder
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
                                            a_map = level)

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
                                            a_map = level)

        assert_that(path, is_(continuous_path(start = (10, 10),
                                              destination = (15, 10),
                                              level = level)))

# TODO: fix this test
class FooTestPathfindingInLevel():
    """
    Test pathfinding in a generated level
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.new_level = None

    def setup(self):
        """
        set up test case
        """
        rng = Random()

        partitioner = GridPartitioner(['crypt'],
                                      1,
                                      1,
                                      rng)
        room_generator = CatacombsGenerator(FLOOR_TILE,
                                            EMPTY_TILE,
                                            ['crypt'],
                                            rng)
        level_decorator = mock()
        portal_adder = PortalAdder((1, 2),
                                   'crypt',
                                   mock(),
                                   False,
                                   rng)
        creature_adder = mock()
        item_adder = mock()

        portal = mock(Portal)

        generator = LevelGenerator(Model(),
                                   partitioner, [room_generator],
                                   level_decorator, [portal_adder],
                                   item_adder,
                                   creature_adder,
                                   rng,
                                   LevelContext(size = (60, 40),
                                                floor_type = FLOOR_TILE,
                                                wall_type = WALL_TILE,
                                                level_types = ['test']))

        self.level = generator.generate_level(portal)

    def test_finding_path(self):
        """
        Test pathfinding in a level
        """
        start = find_free_space(self.level)
        destination = find_free_space(self.level)

        path, connections, updated = a_star(start = start,
                                            goal = destination,
                                            a_map = self.level)

        assert_that(path, is_(continuous_path(start = start,
                                              destination = destination,
                                              level = self.level)))
