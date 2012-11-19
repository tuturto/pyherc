#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
from pyherc.test.builders import LevelBuilder
from pyherc.ai import a_star

from hamcrest import assert_that, contains

FLOOR_TILE = 100
WALL_TILE = 200
EMPTY_TILE = 0

class TestAStar(object):
    """
    Tests for A* path finding
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestAStar, self).__init__()

    def test_simple_path(self):
        """
        Test that a simple path can be found
        """
        level = (LevelBuilder()
                    .with_floor_tile(FLOOR_TILE)
                    .with_wall_tile(EMPTY_TILE)
                    .with_empty_wall_tile(EMPTY_TILE)
                    .with_solid_wall_tile(WALL_TILE)
                    .build())

        path, connections, uptated = a_star(start = (10, 10),
                                            goal = (15, 10),
                                            a_map = level)

        assert_that(path, contains((10, 10),
                                   (11, 10),
                                   (12, 10),
                                   (13, 10),
                                   (14, 10),
                                   (15, 10)))
