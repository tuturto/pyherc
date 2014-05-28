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
Tests for LevelDecorator
"""

from hamcrest import assert_that, equal_to, is_
from mockito import any, mock, verify, when
from pyherc.data import floor_tile, wall_tile, ornamentation, get_tiles
from pyherc.generators.level.decorator import (AggregateDecorator,
                                               AggregateDecoratorConfig,
                                               DirectionalWallDecorator,
                                               DirectionalWallDecoratorConfig,
                                               ReplacingDecorator,
                                               ReplacingDecoratorConfig,
                                               WallBuilderDecorator,
                                               WallBuilderDecoratorConfig,
                                               WallOrnamentDecorator,
                                               WallOrnamentDecoratorConfig)
from pyherc.generators.level.prototiles import (FLOOR_CONSTRUCTED,
                                                FLOOR_NATURAL, WALL_CONSTRUCTED,
                                                WALL_NATURAL)
from pyherc.test.builders import LevelBuilder


class TestLevelDecorator():
    """
    Tests for LevelDecorator
    """
    def __init__(self):
        """
        Default constructor
        """
        self.level = None
        self.config = None
        self.decorator = None
        self.floor_rock = None
        self.floor_brick = None
        self.wall_empty = None
        self.wall_ground = None

    def setup(self):
        """
        Setup the test case
        """
        self.floor_rock = 1
        self.floor_brick = 2
        self.wall_empty = None
        self.wall_ground = 4
        self.level = (LevelBuilder()
                      .with_size((10, 15))
                      .with_floor_tile(FLOOR_NATURAL)
                      .with_wall_tile(self.wall_empty)
                      .build())

        floor_tile(self.level, (5, 5), FLOOR_CONSTRUCTED)
        floor_tile(self.level, (6, 5), FLOOR_CONSTRUCTED)
        floor_tile(self.level, (7, 5), FLOOR_CONSTRUCTED)
        floor_tile(self.level, (0, 0), FLOOR_CONSTRUCTED)
        floor_tile(self.level, (10, 0), FLOOR_CONSTRUCTED)
        floor_tile(self.level, (0, 15), FLOOR_CONSTRUCTED)
        floor_tile(self.level, (10, 15), FLOOR_CONSTRUCTED)

        wall_tile(self.level, (2, 2), WALL_NATURAL)
        wall_tile(self.level, (5, 5), WALL_NATURAL)

        self.config = ReplacingDecoratorConfig(['crypt'],
                                               {FLOOR_NATURAL: self.floor_rock,
                                               FLOOR_CONSTRUCTED: self.floor_brick},
                                               {WALL_NATURAL: self.wall_ground}
                                               )
        self.decorator = ReplacingDecorator(self.config)

    def test_replacing_ground(self):
        """
        Test that proto ground is replaced with given tiles
        """
        self.decorator.decorate_level(self.level)


        assert_that(floor_tile(self.level, (5, 5)), is_(equal_to(self.floor_brick)))
        assert_that(floor_tile(self.level, (6, 5)), is_(equal_to(self.floor_brick)))
        assert_that(floor_tile(self.level, (7, 5)), is_(equal_to(self.floor_brick)))
        assert_that(floor_tile(self.level, (0, 0)), is_(equal_to(self.floor_brick)))
        assert_that(floor_tile(self.level, (10, 0)), is_(equal_to(self.floor_brick)))
        assert_that(floor_tile(self.level, (0, 15)), is_(equal_to(self.floor_brick)))
        assert_that(floor_tile(self.level, (10, 15)), is_(equal_to(self.floor_brick)))

        assert_that(floor_tile(self.level, (2, 2)), is_(equal_to(self.floor_rock)))

    def test_replacing_walls(self):
        """
        Test that proto walls are replaced with given tiles
        """
        self.decorator.decorate_level(self.level)

        assert_that(wall_tile(self.level, (2, 2)), is_(equal_to(self.wall_ground)))
        assert_that(wall_tile(self.level, (5, 5)), is_(equal_to(self.wall_ground)))

class TestWallBuilderDecorator():
    """
    Tests for WallBuilderDecorator
    """
    def __init__(self):
        """
        Default constructor
        """
        self.level = None
        self.config = None
        self.decorator = None
        self.wall_empty = None

    def setup(self):
        """
        Setup the test case
        """
        self.wall_empty = 1
        self.level = (LevelBuilder()
                      .with_size((10, 15))
                      .with_floor_tile(FLOOR_NATURAL)
                      .with_wall_tile(WALL_NATURAL)
                      .build())

        for loc_y in range(2, 8):
            for loc_x in range(2, 8):
                wall_tile(self.level, (loc_x, loc_y), self.wall_empty)

        self.config = WallBuilderDecoratorConfig(['crypt'],
                                            {WALL_NATURAL: WALL_CONSTRUCTED},
                                            self.wall_empty)

        self.decorator = WallBuilderDecorator(self.config)

    def test_building_walls(self):
        """
        Test that tiles next to empty space are replaced
        """
        self.decorator.decorate_level(self.level)

        for loc in range(2, 8):
            assert_that(wall_tile(self.level, (loc, 1)),
                        is_(equal_to(WALL_CONSTRUCTED)))
            assert_that(wall_tile(self.level, (loc, 8)),
                        is_(equal_to(WALL_CONSTRUCTED)))
            assert_that(wall_tile(self.level, (1, loc)),
                        is_(equal_to(WALL_CONSTRUCTED)))
            assert_that(wall_tile(self.level, (8, loc)),
                        is_(equal_to(WALL_CONSTRUCTED)))

        assert_that(wall_tile(self.level, (0, 0)),
                    is_(equal_to(WALL_NATURAL)))

class TestAggregateDecorator():
    """
    Tests for AggregateDecorator
    """
    def __init__(self):
        """
        Default constructor
        """
        self.level = None
        self.mock_decorator_1 = None
        self.mock_decorator_2 = None
        self.config = None
        self.decorator = None

    def setup(self):
        """
        Setup the testcase
        """
        self.level = LevelBuilder().build()

        self.mock_decorator_1 = mock(WallBuilderDecorator)
        self.mock_decorator_2 = mock(ReplacingDecorator)

        self.config = AggregateDecoratorConfig(['crypt'],
                                               [self.mock_decorator_1,
                                               self.mock_decorator_2])
        self.decorator = AggregateDecorator(self.config)

    def test_subdecorators_are_called(self):
        """
        Test that sub decorators of aggregate decorator are called
        """
        self.decorator.decorate_level(self.level)

        verify(self.mock_decorator_1).decorate_level(self.level)
        verify(self.mock_decorator_2).decorate_level(self.level)

class TestDirectionalWallDecorator():
    """
    Test that directional walls can be decorated
    """
    def __init__(self):
        """
        Default constructor
        """
        self.level = None
        self.config = None
        self.decorator = None

        self.empty_wall = None
        self.wall = 'wall'

    def setup(self):
        """
        Setup the test case
        """
        self.level = (LevelBuilder()
                      .with_size((10, 10))
                      .with_floor_tile('floor')
                      .with_wall_tile(self.empty_wall)
                      .build())

        wall_tile(self.level, (1, 1), self.wall)
        wall_tile(self.level, (2, 1), self.wall)
        wall_tile(self.level, (3, 1), self.wall)

        wall_tile(self.level, (1, 2), self.wall)
        wall_tile(self.level, (1, 3), self.wall)

        wall_tile(self.level, (2, 3), self.wall)
        wall_tile(self.level, (3, 3), self.wall)

        wall_tile(self.level, (3, 2), self.wall)

        self.config = DirectionalWallDecoratorConfig(level_types = ['crypt'],
                                                   east_west = 'east-west',
                                                   east_north = 'east-north',
                                                   east_south = 'east-south',
                                                   west_north = 'west-north',
                                                   west_south = 'west-south',
                                                   north_south = 'north-south',
                                                   east_west_north = 'east-west-north',
                                                   east_west_south = 'east-west-south',
                                                   east_north_south = 'east-north-south',
                                                   west_north_south = 'west-north-south',
                                                   four_way = 'four-way',
                                                   wall = self.wall)

        self.decorator = DirectionalWallDecorator(self.config)

    def test_building_basic_walls(self):
        """
        Test that basic wall can be built
        """
        self.decorator.decorate_level(self.level)

        assert_that(wall_tile(self.level, (1, 1)), is_(equal_to('east-south')))
        assert_that(wall_tile(self.level, (2, 1)), is_(equal_to('east-west')))
        assert_that(wall_tile(self.level, (3, 1)), is_(equal_to('west-south')))
        assert_that(wall_tile(self.level, (1, 2)), is_(equal_to('north-south')))
        assert_that(wall_tile(self.level, (1, 3)), is_(equal_to('east-north')))
        assert_that(wall_tile(self.level, (3, 3)), is_(equal_to('west-north')))

class TestDecoratingWallOrnaments():
    """
    Test that walls can be ornamented
    """
    def __init__(self):
        """
        Default constructor
        """
        self.level = None
        self.config = None
        self.decorator = None

        self.empty_wall = None
        self.empty_floor = None
        self.wall = None
        self.floor = None
        self.ornament = None

    def setup(self):
        """
        Setup test cases
        """
        self.empty_wall = None
        self.empty_floor = None
        self.wall = 'wall'
        self.floor = 'floor'
        self.ornamentation = 'candles'

        self.level = (LevelBuilder()
                      .with_size((10, 10))
                      .with_floor_tile(self.floor)
                      .with_wall_tile(self.empty_wall)
                      .build())

    def test_walls_can_be_ornamented(self):
        """
        Ornaments should be placed only on walls
        """
        wall_tile(self.level, (2, 2), self.wall)
        wall_tile(self.level, (3, 2), self.wall)
        wall_tile(self.level, (3, 2), self.wall)

        rng = mock()
        when(rng).randint(any(), any()).thenReturn(0)
        when(rng).choice(any()).thenReturn(self.ornamentation)

        self.config = WallOrnamentDecoratorConfig(
                                        ['any level'],
                                        wall_tile = self.wall,
                                        ornamentation = [self.ornamentation],
                                        rng = rng,
                                        rate = 100)
        self.decorator = WallOrnamentDecorator(self.config)

        self.decorator.decorate_level(self.level)

        assert_that(ornamentation(self.level, (2, 2)),
                    is_(equal_to(self.ornamentation)))

    def test_ornamentation_rate_can_be_controlled(self):
        """
        There should be way to control how frequently walls are ornamented
        """
        wall_tile(self.level, (2, 2), self.wall)
        wall_tile(self.level, (3, 2), self.wall)
        wall_tile(self.level, (4, 2), self.wall)

        rng = mock()
        when(rng).randint(any(), any()).thenReturn(0).thenReturn(100).thenReturn(0)
        when(rng).choice(any()).thenReturn(self.ornamentation)

        self.config = WallOrnamentDecoratorConfig(
                                        ['any level'],
                                        wall_tile = self.wall,
                                        ornamentation = [self.ornamentation],
                                        rng = rng,
                                        rate = 50)
        self.decorator = WallOrnamentDecorator(self.config)

        self.decorator.decorate_level(self.level)

        candle_count = 0
        for location, tile in get_tiles(self.level):
            if tile['\ufdd0:ornamentation'] == self.ornamentation:
                candle_count = candle_count + 1

        assert_that(candle_count, is_(equal_to(2)))

    def test_only_northern_wall_is_decorated(self):
        """
        Ornamentations should be placed only on northern walls
        """
        wall_tile(self.level, (2, 2), self.wall)
        wall_tile(self.level, (3, 2), self.wall)
        wall_tile(self.level, (4, 2), self.wall)

        floor_tile(self.level, (2, 3), self.floor)
        floor_tile(self.level, (3, 3), self.floor)
        floor_tile(self.level, (4, 3), self.floor)

        wall_tile(self.level, (2, 4), self.wall)
        wall_tile(self.level, (3, 4), self.wall)
        wall_tile(self.level, (4, 4), self.wall)

        floor_tile(self.level, (2, 5), self.empty_floor)
        floor_tile(self.level, (4, 5), self.empty_floor)
        floor_tile(self.level, (4, 5), self.empty_floor)

        rng = mock()
        when(rng).randint(any(), any()).thenReturn(0)
        when(rng).choice(any()).thenReturn(self.ornamentation)

        self.config = WallOrnamentDecoratorConfig(
                                        ['any level'],
                                        wall_tile = self.wall,
                                        ornamentation = [self.ornamentation],
                                        rng = rng,
                                        rate = 100)

        self.decorator = WallOrnamentDecorator(self.config)

        self.decorator.decorate_level(self.level)

        assert_that(ornamentation(self.level, (2, 2)),
                    is_(equal_to(self.ornamentation)))
        assert_that(ornamentation(self.level, (2, 4)),
                    is_(equal_to(None)))
