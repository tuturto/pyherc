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
#pylint: disable=W0614
from hamcrest import assert_that, equal_to, is_  # pylint: disable-msg=E0611
from mockito import any, mock, verify, when
from pyherc.data import Level
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
        self.wall_empty = 3
        self.wall_ground = 4
        self.level = Level(mock(), (10, 15),
                      floor_type = FLOOR_NATURAL,
                      wall_type = self.wall_empty)

        self.level.floor[5][5] = FLOOR_CONSTRUCTED
        self.level.floor[6][5] = FLOOR_CONSTRUCTED
        self.level.floor[7][5] = FLOOR_CONSTRUCTED
        self.level.floor[0][0] = FLOOR_CONSTRUCTED
        self.level.floor[10][0] = FLOOR_CONSTRUCTED
        self.level.floor[0][15] = FLOOR_CONSTRUCTED
        self.level.floor[10][15] = FLOOR_CONSTRUCTED

        self.level.walls[2][2] = WALL_NATURAL
        self.level.walls[5][5] = WALL_NATURAL

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

        assert_that(self.level.floor[5][5], is_(equal_to(self.floor_brick)))
        assert_that(self.level.floor[6][5], is_(equal_to(self.floor_brick)))
        assert_that(self.level.floor[7][5], is_(equal_to(self.floor_brick)))
        assert_that(self.level.floor[0][0], is_(equal_to(self.floor_brick)))
        assert_that(self.level.floor[10][0], is_(equal_to(self.floor_brick)))
        assert_that(self.level.floor[0][15], is_(equal_to(self.floor_brick)))
        assert_that(self.level.floor[10][15], is_(equal_to(self.floor_brick)))

        assert_that(self.level.floor[2][2], is_(equal_to(self.floor_rock)))

    def test_replacing_walls(self):
        """
        Test that proto walls are replaced with given tiles
        """
        self.decorator.decorate_level(self.level)

        assert_that(self.level.walls[2][2], is_(equal_to(self.wall_ground)))
        assert_that(self.level.walls[5][5], is_(equal_to(self.wall_ground)))

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
        self.level = Level(mock(), (10, 15),
                      floor_type = FLOOR_NATURAL,
                      wall_type = WALL_NATURAL)

        for loc_y in range(2, 8):
            for loc_x in range(2, 8):
                self.level.walls[loc_x][loc_y] = self.wall_empty

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
            assert_that(self.level.walls[loc][1],
                        is_(equal_to(WALL_CONSTRUCTED)))
            assert_that(self.level.walls[loc][8],
                        is_(equal_to(WALL_CONSTRUCTED)))
            assert_that(self.level.walls[1][loc],
                        is_(equal_to(WALL_CONSTRUCTED)))
            assert_that(self.level.walls[8][loc],
                        is_(equal_to(WALL_CONSTRUCTED)))

        assert_that(self.level.walls[0][0], is_(equal_to(WALL_NATURAL)))

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
        self.level = mock(Level)
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
        self.empty_wall = 'empty space'
        self.level = Level(mock(), (10, 10),
                           floor_type = 'floor',
                           wall_type = self.empty_wall)

        self.level.walls[1][1] = self.wall
        self.level.walls[2][1] = self.wall
        self.level.walls[3][1] = self.wall

        self.level.walls[1][2] = self.wall
        self.level.walls[1][3] = self.wall

        self.level.walls[2][3] = self.wall
        self.level.walls[3][3] = self.wall

        self.level.walls[3][2] = self.wall

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

        assert_that(self.level.walls[1][1], is_(equal_to('east-south')))
        assert_that(self.level.walls[2][1], is_(equal_to('east-west')))
        assert_that(self.level.walls[3][1], is_(equal_to('west-south')))
        assert_that(self.level.walls[1][2], is_(equal_to('north-south')))
        assert_that(self.level.walls[1][3], is_(equal_to('east-north')))
        assert_that(self.level.walls[3][3], is_(equal_to('west-north')))

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

        self.level = Level(mock(), (10, 10),
                           floor_type = self.floor,
                           wall_type = self.empty_wall)

    def test_walls_can_be_ornamented(self):
        """
        Ornaments should be placed only on walls
        """
        self.level.set_wall_tile(2, 2, self.wall)
        self.level.set_wall_tile(3, 2, self.wall)
        self.level.set_wall_tile(4, 2, self.wall)

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

        assert_that(self.level.ornamentations[2][2],
                    is_(equal_to(self.ornamentation)))

    def test_ornamentation_rate_can_be_controlled(self):
        """
        There should be way to control how frequently walls are ornamented
        """
        self.level.set_wall_tile(2, 2, self.wall)
        self.level.set_wall_tile(3, 2, self.wall)
        self.level.set_wall_tile(4, 2, self.wall)

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

        assert_that(self.level.ornamentations[2][2],
                    is_(equal_to(self.ornamentation)))
        assert_that(self.level.ornamentations[3][2],
                    is_(equal_to(None)))
        assert_that(self.level.ornamentations[4][2],
                    is_(equal_to(self.ornamentation)))

    def test_only_northern_wall_is_decorated(self):
        """
        Ornamentations should be placed only on northern walls
        """
        self.level.set_wall_tile(2, 2, self.wall)
        self.level.set_wall_tile(3, 2, self.wall)
        self.level.set_wall_tile(4, 2, self.wall)

        self.level.set_floor_tile(2, 3, self.floor)
        self.level.set_floor_tile(3, 3, self.floor)
        self.level.set_floor_tile(4, 3, self.floor)

        self.level.set_wall_tile(2, 4, self.wall)
        self.level.set_wall_tile(3, 4, self.wall)
        self.level.set_wall_tile(4, 4, self.wall)

        self.level.set_floor_tile(2, 5, self.empty_floor)
        self.level.set_floor_tile(3, 5, self.empty_floor)
        self.level.set_floor_tile(4, 5, self.empty_floor)

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

        assert_that(self.level.ornamentations[2][2],
                    is_(equal_to(self.ornamentation)))
        assert_that(self.level.ornamentations[2][4],
                    is_(equal_to(None)))
