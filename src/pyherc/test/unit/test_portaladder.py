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
Module for testing PortalAdder functionality
"""
import random

from hamcrest import assert_that, equal_to, is_, has_length
from mockito import mock
from pyherc.data import Level
from pyherc.generators.level.generator import LevelGenerator
from pyherc.generators.level.portals import (PortalAdder,
                                             PortalAdderConfiguration,
                                             PortalAdderFactory)
from pyherc.test.matchers import located_in_room


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
        self.wall_empty = 10

    def test_add_stairs_to_room(self):
        """
        Test that stairs can be added to a room
        """
        level = Level(size = (20, 20),
                      floor_type = self.floor_rock,
                      wall_type = self.wall_empty)

        for loc_y in range(8, 12):
            for loc_x in range(8, 12):
                level.set_location_type((loc_x, loc_y), 'room')

        portal_adder = PortalAdder((1, 2),
                                   'room',
                                   mock(),
                                   False,
                                   self.rng)

        portal_adder.add_portal(level)

        portals = level.portals
        assert_that(portals, has_length(1))
        portal = level.portals[0]
        assert_that(located_in_room(portal), is_(True))

    def test_portal_has_icons(self):
        """
        Test that portal created by adder has two icons set
        One to display and another to be used by opposite end
        """
        level = Level(size = (20, 20),
                      floor_type = self.floor_rock,
                      wall_type = self.wall_empty)

        level_generator = mock(LevelGenerator)

        for loc_y in range(8, 12):
            for loc_x in range(8, 12):
                level.set_location_type((loc_x, loc_y), 'room')

        portal_adder = PortalAdder((1, 2),
                                   'room',
                                   level_generator,
                                   False,
                                   self.rng)

        portal_adder.add_portal(level)

        portals = level.portals
        portal = level.portals[0]

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
