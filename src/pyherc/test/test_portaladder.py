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
Module for testing PortalAdder functionality
"""
#pylint: disable=W0614
from pyherc.data.tiles import FLOOR_ROCK, WALL_EMPTY
from pyherc.data import Level, Portal
from pyherc.generators.level.portals import PortalAdder, PortalAdderFactory
from pyherc.generators.level.portals import PortalAdderConfiguration
from hamcrest import * #pylint: disable=W0401
from pyherc.test.matchers import * #pylint: disable=W0401
from pyDoubles.framework import empty_stub #pylint: disable=F0401, E0611
import random

class TestPortalAdder():
    """
    Tests for PortalAdder
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
                level.set_location_type((loc_x, loc_y), 'room')

        portal_adder = PortalAdder('room',
                                   self.rng)

        portal_adder.add_stairs(level)

        portals = level.portals
        assert_that(portals, has_length(1))
        portal = level.portals[0]
        assert_that(located_in_room(portal), is_(True))

class TestPortalAdderFactory():
    """
    Tests for PortalAdderFactory
    """
    def __init__(self):
        """
        Default constructor
        """
        self.rng = None

    def setup(self):
        """
        Setup the test case
        """
        self.rng = random.Random()

    def test_create_portal_adder(self):
        """
        Test that factory can create a portal adder
        """
        portal_config = PortalAdderConfiguration(level_type = 'catacombs',
                                                 location_type = 'room',
                                                 chance = 100,
                                                 new_level = 'upper crypt',
                                                 unique = False)

        factory = PortalAdderFactory([portal_config],
                                     self.rng)

        portal_adders = factory.create_portal_adders('catacombs')

        assert_that(portal_adders, has_length(1))
