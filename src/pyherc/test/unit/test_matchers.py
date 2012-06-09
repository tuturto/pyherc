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
Module for testing customer matchers
"""
#pylint: disable=W0614
from pyherc.data import Level
from pyherc.data.tiles import WALL_EMPTY, FLOOR_ROCK, WALL_GROUND
from pyherc.test.matchers.map_connectivity import MapConnectivity
from pyherc.data import EffectsCollection
from pyherc.rules.effects import EffectHandle
from pyherc.test.matchers.effect_collection import ContainsEffectHandle
from hamcrest import * #pylint: disable=W0401
from mockito import *  #pylint: disable=W0401

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

class TestContainsEffectHandle(object):
    """
    Tests for ContainsEffectHandle matcher
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestContainsEffectHandle, self).__init__()

    def test_match_single_handle(self):
        """
        Test that single handle can be matched
        """
        collection = EffectsCollection()
        handle = EffectHandle(trigger = 'on drink',
                              effect = None,
                              parameters = None,
                              charges = 1)

        collection.add_effect_handle(handle)

        matcher = ContainsEffectHandle(handle)

        assert_that(matcher._matches(collection), is_(equal_to(True)))

    def test_detect_sinle_mismatch(self):
        """
        Test that missing a single handle is detected correctly
        """
        collection = EffectsCollection()
        handle1 = EffectHandle(trigger = 'on drink',
                               effect = None,
                               parameters = None,
                               charges = 1)

        collection.add_effect_handle(handle1)

        handle2 = EffectHandle(trigger = 'on kick',
                               effect = None,
                               parameters = None,
                               charges = 1)

        matcher = ContainsEffectHandle(handle2)

        assert_that(matcher._matches(collection), is_(equal_to(False)))

    def test_match_multiple_handles(self):
        """
        Test that matcher can match multiple handlers
        """
        collection = EffectsCollection()
        handle1 = EffectHandle(trigger = 'on drink',
                               effect = None,
                               parameters = None,
                               charges = 1)

        handle2 = EffectHandle(trigger = 'on kick',
                               effect = None,
                               parameters = None,
                               charges = 1)

        collection.add_effect_handle(handle1)
        collection.add_effect_handle(handle2)

        matcher = ContainsEffectHandle([handle1, handle2])

        assert_that(matcher._matches(collection), is_(equal_to(True)))

    def test_detect_mismatch_in_collection(self):
        """
        Test that matcher can detect a mismatch in collection
        """
        collection = EffectsCollection()
        handle1 = EffectHandle(trigger = 'on drink',
                               effect = None,
                               parameters = None,
                               charges = 1)

        handle2 = EffectHandle(trigger = 'on kick',
                               effect = None,
                               parameters = None,
                               charges = 1)

        handle3 = EffectHandle(trigger = 'on burn',
                               effect = None,
                               parameters = None,
                               charges = 1)

        collection.add_effect_handle(handle1)
        collection.add_effect_handle(handle2)

        matcher = ContainsEffectHandle([handle1, handle2, handle3])

        assert_that(matcher._matches(collection), is_(equal_to(False)))

    def test_mismatch_any(self):
        """
        Test that matcher can mismatch to any handle
        """
        collection = EffectsCollection()

        matcher = ContainsEffectHandle(None)

        assert_that(matcher._matches(collection), is_(equal_to(False)))

    def test_match_any(self):
        """
        Test that matcher can match to any handle
        """
        collection = EffectsCollection()
        handle1 = EffectHandle(trigger = 'on drink',
                               effect = None,
                               parameters = None,
                               charges = 1)

        collection.add_effect_handle(handle1)

        matcher = ContainsEffectHandle(None)

        assert_that(matcher._matches(collection), is_(equal_to(True)))
