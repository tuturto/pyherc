# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Module for testing PortalAdder functionality
"""
import random

from hamcrest import assert_that, equal_to, has_length, is_
from mockito import mock
from pyherc.data import get_portal, add_location_tag
from pyherc.generators.level.portal import (PortalAdder,
                                            PortalAdderConfiguration,
                                            PortalAdderFactory)
from pyherc.test.matchers import located_in_room
from pyherc.test.builders import LevelBuilder


class TestPortalAdder():
    """
    Tests for PortalAdder
    """
    def __init__(self):
        """
        Default constructor
        """
        self.rng = None
        self.floor_rock = None
        self.wall_empty = None

    def setup(self):
        """
        Setup test case
        """
        self.rng = random.Random()
        self.floor_rock = 1
        self.wall_empty = None

    def test_add_stairs_to_room(self):
        """
        Test that stairs can be added to a room
        """
        level = (LevelBuilder()
                 .with_size((20, 20))
                 .with_floor_tile(self.floor_rock)
                 .with_wall_tile(self.wall_empty)
                 .build())

        for loc_y in range(8, 12):
            for loc_x in range(8, 12):
                add_location_tag(level, (loc_x, loc_y), 'room')

        portal_adder = PortalAdder((1, 2),
                                   'room',
                                   mock(),
                                   False,
                                   self.rng)

        portal_adder.add_portal(level)

        portals = []
        for loc_y in range(8, 12):
            for loc_x in range(8, 12):
                temp = get_portal(level, (loc_x, loc_y))
                if temp:
                    portals.append(temp)

        assert_that(portals, has_length(1))
        portal = portals[0]
        assert_that(located_in_room(portal), is_(True))

    def test_portal_has_icons(self):
        """
        Test that portal created by adder has two icons set
        One to display and another to be used by opposite end
        """
        level = (LevelBuilder()
                 .with_size((20, 20))
                 .with_floor_tile(self.floor_rock)
                 .with_wall_tile(self.wall_empty)
                 .build())

        level_generator = mock()

        for loc_y in range(8, 12):
            for loc_x in range(8, 12):
                add_location_tag(level, (loc_x, loc_y), 'room')

        portal_adder = PortalAdder((1, 2),
                                   'room',
                                   level_generator,
                                   False,
                                   self.rng)

        portal_adder.add_portal(level)

        portals = []
        for loc_y in range(8, 12):
            for loc_x in range(8, 12):
                temp = get_portal(level, (loc_x, loc_y))
                if temp:
                    portals.append(temp)
        portal = portals[0]

        assert_that(portal.icon, is_(equal_to(1)))
        assert_that(portal.other_end_icon, is_(equal_to(2)))

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
        portal_config = [PortalAdderConfiguration(icons = (1, 2),
                                                  level_type = 'catacombs',
                                                  location_type = 'room',
                                                  chance = 100,
                                                  new_level = 'upper crypt',
                                                  unique = False)]

        factory = PortalAdderFactory(portal_config,
                                     self.rng)
        factory.level_generator_factory = mock()

        portal_adders = factory.create_portal_adders('catacombs')

        assert_that(portal_adders, has_length(1))

    def test_multiple_adders_can_be_returned(self):
        """
        Test that portal adder factory respects level type
        """
        portal_config = [PortalAdderConfiguration(icons = (1, 2),
                                                  level_type = 'catacombs',
                                                  location_type = 'room',
                                                  chance = 100,
                                                  new_level = 'upper crypt',
                                                  unique = False),
                         PortalAdderConfiguration(icons = (1, 2),
                                                  level_type = 'catacombs',
                                                  location_type = 'room',
                                                  chance = 100,
                                                  new_level = 'dungeon',
                                                  unique = False)
                                                 ]

        factory = PortalAdderFactory(portal_config,
                                     self.rng)
        factory.level_generator_factory = mock()

        portal_adders = factory.create_portal_adders('catacombs')

        assert_that(portal_adders, has_length(2))

    def test_level_type_is_respected(self):
        """
        Test that portal adder factory respects level type
        """
        portal_config = [PortalAdderConfiguration(icons = (1, 2),
                                                  level_type = 'catacombs',
                                                  location_type = 'room',
                                                  chance = 100,
                                                  new_level = 'upper crypt',
                                                  unique = False),
                         PortalAdderConfiguration(icons = (1, 2),
                                                  level_type = 'upper crypt',
                                                  location_type = 'room',
                                                  chance = 100,
                                                  new_level = 'lower crypt',
                                                  unique = False)
                                                 ]

        factory = PortalAdderFactory(portal_config,
                                     self.rng)
        factory.level_generator_factory = mock()

        portal_adders = factory.create_portal_adders('catacombs')

        assert_that(portal_adders, has_length(1))

    def test_handling_no_matches(self):
        """
        Test that portal adder factory graciously returns empty list when
        no match has been found
        """
        portal_config = [PortalAdderConfiguration(icons = (1, 2),
                                                  level_type = 'catacombs',
                                                  location_type = 'room',
                                                  chance = 100,
                                                  new_level = 'upper crypt',
                                                  unique = False),
                         PortalAdderConfiguration(icons = (1, 2),
                                                  level_type = 'upper crypt',
                                                  location_type = 'room',
                                                  chance = 100,
                                                  new_level = 'lower crypt',
                                                  unique = False)
                                                 ]

        factory = PortalAdderFactory(portal_config,
                                     self.rng)

        portal_adders = factory.create_portal_adders('castle')

        assert_that(portal_adders, has_length(0))

    def test_removing_unique_portal_adders(self):
        """
        Test that unique portal adder specificatin is removed from configuration
        after it has been used first time
        """
        portal_config = [PortalAdderConfiguration(icons = (1, 2),
                                                  level_type = 'catacombs',
                                                  location_type = 'room',
                                                  chance = 100,
                                                  new_level = 'upper crypt',
                                                  unique = True),
                         PortalAdderConfiguration(icons = (1, 2),
                                                  level_type = 'upper crypt',
                                                  location_type = 'room',
                                                  chance = 100,
                                                  new_level = 'lower crypt',
                                                  unique = False)
                                                 ]

        factory = PortalAdderFactory(portal_config,
                                     self.rng)
        factory.level_generator_factory = mock()

        portal_adders = factory.create_portal_adders('catacombs')

        assert_that(factory.config, has_length(1))

    def test_level_generator_is_created(self):
        """
        Test that portal adder has level generator set to it
        """
        portal_config = [PortalAdderConfiguration(icons = (1, 2),
                                                  level_type = 'catacombs',
                                                  location_type = 'room',
                                                  chance = 100,
                                                  new_level = 'upper crypt',
                                                  unique = False)]

        factory = PortalAdderFactory(portal_config,
                                     self.rng)

        portal_adders = factory.create_portal_adders('catacombs')

        portal_adder = portal_adders[0]

        assert_that(portal_adder.level_generator_name,
                    is_(equal_to('upper crypt')))
