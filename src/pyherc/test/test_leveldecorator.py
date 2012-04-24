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
Tests for LevelDecorator
"""
#pylint: disable=W0614
from pyherc.generators.level.decorator import ReplacingDecorator
from pyherc.generators.level.decorator import ReplacingDecoratorConfig
from pyherc.generators.level.decorator import WallBuilderDecorator
from pyherc.generators.level.decorator import WallBuilderDecoratorConfig
from pyherc.generators.level.decorator import AggregateDecorator
from pyherc.generators.level.decorator import AggregateDecoratorConfig
from pyherc.data import Level
from mockito import mock, verify
from hamcrest import * #pylint: disable=W0401
from pyherc.data.tiles import FLOOR_ROCK, FLOOR_BRICK, WALL_EMPTY, WALL_GROUND
from pyherc.generators.level.prototiles import FLOOR_NATURAL, FLOOR_CONSTRUCTED
from pyherc.generators.level.prototiles import WALL_NATURAL, WALL_CONSTRUCTED

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

    def setup(self):
        """
        Setup the test case
        """
        self.level = Level((10, 15),
                      floor_type = FLOOR_NATURAL,
                      wall_type = WALL_EMPTY)

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
                                               {FLOOR_NATURAL: FLOOR_ROCK,
                                               FLOOR_CONSTRUCTED: FLOOR_BRICK},
                                               {WALL_NATURAL: WALL_GROUND}
                                               )
        self.decorator = ReplacingDecorator(self.config)

    def test_replacing_ground(self):
        """
        Test that proto ground is replaced with given tiles
        """
        self.decorator.decorate_level(self.level)

        assert_that(self.level.floor[5][5], is_(equal_to(FLOOR_BRICK)))
        assert_that(self.level.floor[6][5], is_(equal_to(FLOOR_BRICK)))
        assert_that(self.level.floor[7][5], is_(equal_to(FLOOR_BRICK)))
        assert_that(self.level.floor[0][0], is_(equal_to(FLOOR_BRICK)))
        assert_that(self.level.floor[10][0], is_(equal_to(FLOOR_BRICK)))
        assert_that(self.level.floor[0][15], is_(equal_to(FLOOR_BRICK)))
        assert_that(self.level.floor[10][15], is_(equal_to(FLOOR_BRICK)))

        assert_that(self.level.floor[2][2], is_(equal_to(FLOOR_ROCK)))

    def test_replacing_walls(self):
        """
        Test that proto walls are replaced with given tiles
        """
        self.decorator.decorate_level(self.level)

        assert_that(self.level.walls[2][2], is_(equal_to(WALL_GROUND)))
        assert_that(self.level.walls[5][5], is_(equal_to(WALL_GROUND)))

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

    def setup(self):
        """
        Setup the test case
        """
        self.level = Level((10, 15),
                      floor_type = FLOOR_NATURAL,
                      wall_type = WALL_NATURAL)

        for loc_y in range(2, 8):
            for loc_x in range(2, 8):
                self.level.walls[loc_x][loc_y] = WALL_EMPTY

        self.config = WallBuilderDecoratorConfig(['crypt'],
                                            {WALL_NATURAL: WALL_CONSTRUCTED},
                                            WALL_EMPTY)

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
