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
Module for testing StairAdder functionality
"""
#pylint: disable=W0614
from pyherc.data.tiles import FLOOR_ROCK, WALL_EMPTY
from pyherc.data import Level, Portal
from pyherc.generators.level.stairs import StairAdder
from hamcrest import * #pylint: disable=W0401
from pyherc.test.matchers import * #pylint: disable=W0401
import random

class TestStairAdder():
    """
    Tests for StairAdder
    """
    def __init__(self):
        """
        Default constructor
        """
        self.rng = None

    def setup(self):
        """
        Setup test case
        """
        self.rng = random.Random()

    def test_add_stairs_to_room(self):
        """
        Test that stairs can be added to a room
        """
        level = Level(size = (20, 20),
                      floor_type = FLOOR_ROCK,
                      wall_type = WALL_EMPTY)

        for loc_y in range(8, 12):
            for loc_x in range(8, 12):
                level.set_room((loc_x, loc_y), True)

        stair_adder = StairAdder(level, self.rng)

        portal = Portal()

        stair_adder.add_stairs(portal)

        portals = level.portals
        assert_that(portals, has_length(1))
        assert_that(located_in_room(portal), is_(True))
