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
Module for testing customer matchers
"""
#pylint: disable=W0614
from pyherc.data import Level
from pyherc.data.tiles import WALL_EMPTY, FLOOR_ROCK, WALL_GROUND
from pyherc.test.matchers.map_connectivity import MapConnectivity
from hamcrest import * #pylint: disable=W0401

class TestLevelConnectivity():
    """
    Class for testing level connectivity matcher
    """
    def __init__(self):
        """
        Default constructor
        """
        self.level = None
        self.matcher = None

    def setup(self):
        """
        Setup the tests
        """
        self.level = Level(size = (20, 10),
                      floor_type = FLOOR_ROCK,
                      wall_type = WALL_GROUND)
        self.matcher = MapConnectivity(WALL_EMPTY)

    def test_unconnected_level(self):
        """
        Test that unconnected level is reported correctly
        """
        for loc_x in range(2, 5):
            self.level.walls[loc_x][2] = WALL_EMPTY
            self.level.walls[loc_x][5] = WALL_EMPTY

        assert_that(self.matcher._matches(self.level), is_(equal_to(False)))

    def test_connected_level(self):
        """
        Test that connected level is reported correctly
        """
        for loc_x in range(2, 8):
            self.level.walls[loc_x][3] = WALL_EMPTY
            self.level.walls[loc_x][5] = WALL_EMPTY
            self.level.walls[5][loc_x] = WALL_EMPTY

        assert_that(self.matcher._matches(self.level), is_(equal_to(True)))

    def test_that_all_points_are_found(self):
        """
        Test that connectivity can find all open points
        """
        self.level.walls[0][0] = WALL_EMPTY
        self.level.walls[5][5] = WALL_EMPTY
        self.level.walls[20][10] = WALL_EMPTY

        points = self.matcher.get_all_points(self.level, WALL_EMPTY)

        assert_that(points, has_length(3))

    def test_that_open_corners_work(self):
        """
        Test that finding connectivity with open corners work
        """
        self.level.walls[0][0] = WALL_EMPTY
        self.level.walls[20][0] = WALL_EMPTY
        self.level.walls[0][10] = WALL_EMPTY
        self.level.walls[20][10] = WALL_EMPTY

        assert_that(self.matcher._matches(self.level), is_(equal_to(False)))

    def test_that_convoluted_case_works(self):
        """
        Test a convoluted case with 3 open areas and 2 of them being connected
        to border
        """
        self.level = Level(size = (10, 10),
                      floor_type = FLOOR_ROCK,
                      wall_type = WALL_GROUND)

        self.level.walls[2][5] = WALL_EMPTY
        self.level.walls[2][6] = WALL_EMPTY
        self.level.walls[2][7] = WALL_EMPTY
        self.level.walls[2][8] = WALL_EMPTY
        self.level.walls[2][9] = WALL_EMPTY
        self.level.walls[2][10] = WALL_EMPTY

        self.level.walls[5][8] = WALL_EMPTY

        self.level.walls[5][2] = WALL_EMPTY
        self.level.walls[6][2] = WALL_EMPTY
        self.level.walls[7][2] = WALL_EMPTY
        self.level.walls[8][2] = WALL_EMPTY
        self.level.walls[9][2] = WALL_EMPTY
        self.level.walls[10][2] = WALL_EMPTY

        all_points = self.matcher.get_all_points(self.level, WALL_EMPTY)
        connected_points = self.matcher.get_connected_points(self.level,
                                                all_points[0],
                                                WALL_EMPTY,
                                                [])

        print 'all points: {0}'.format(all_points)
        print 'connected points: {0}'.format(connected_points)

        assert_that(self.matcher._matches(self.level), is_(equal_to(False)))
