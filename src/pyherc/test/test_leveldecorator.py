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
from pyherc.generators.level.decorator import Decorator, DecoratorConfig
from pyherc.data import Level
from pyDoubles.framework import when, spy, stub #pylint: disable=F0401, E0611
from hamcrest import * #pylint: disable=W0401
from pyherc.data.tiles import FLOOR_ROCK, FLOOR_BRICK, WALL_EMPTY, WALL_GROUND
from pyherc.generators.level.prototiles import FLOOR_NATURAL, FLOOR_CONSTRUCTED
from pyherc.generators.level.prototiles import WALL_NATURAL

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

        self.config = DecoratorConfig()
        self.config.ground_config[FLOOR_NATURAL] = FLOOR_ROCK
        self.config.ground_config[FLOOR_CONSTRUCTED] = FLOOR_BRICK

        self.config.wall_config[WALL_NATURAL] = WALL_GROUND

        self.decorator = Decorator(self.config, self.level)

    def test_replacing_ground(self):
        """
        Test that proto ground is replaced with given tiles
        """
        self.decorator.decorate_level()

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
        self.decorator.decorate_level()

        assert_that(self.level.walls[2][2], is_(equal_to(WALL_GROUND)))
        assert_that(self.level.walls[5][5], is_(equal_to(WALL_GROUND)))
