#!/usr/bin/env python3
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
Tests for CreatureAdder
"""
#pylint: disable=W0614
from mockito import mock
from hamcrest import assert_that, has_length, greater_than, less_than #pylint: disable-msg=E0611
from hamcrest import greater_than_or_equal_to #pylint: disable-msg=E0611
from pyherc.test.matchers import has_creature, located_in_room

from pyherc.data import Level
from pyherc.generators.creature import CreatureGenerator
from pyherc.generators.level.creatures import CreatureAdder
from pyherc.generators.level.creatures import CreatureAdderConfiguration
from pyherc.generators import CreatureConfiguration
import random

class TestCreatureAdder():
    """
    Tests for CreatureAdder
    """
    def __init__(self):
        """
        Default constructor
        """
        self.rng = None
        self.level = None
        self.creature_generator = None
        self.configuration = None
        self.creature_adder = None

    def setup(self):
        """
        Setup the test case
        """
        self.rng = random.Random()
        self.level = Level((60, 40))
        self.level.set_location_type((10, 10), 'room')

        creature_config = {}
        creature_config['rat'] = CreatureConfiguration(name = 'rat',
                                                       body = 4,
                                                       finesse = 12,
                                                       mind = 2,
                                                       hp = 2,
                                                       speed = 2,
                                                       icons = 1,
                                                       attack = 2,
                                                       ai = None)

        creature_config['dragon'] = CreatureConfiguration(
                                              name = 'dragon',
                                              body = 4,
                                              finesse = 12,
                                              mind = 2,
                                              hp = 2,
                                              speed = 2,
                                              icons = 1,
                                              attack = 2,
                                              ai = None)

        self.model = mock()
        self.creature_generator = CreatureGenerator(creature_config,
                                                    self.model,
                                                    mock(),
                                                    self.rng)

        self.configuration = CreatureAdderConfiguration(['crypt'])
        self.configuration.add_creature(min_amount = 3,
                                        max_amount = 4,
                                        name = 'rat')
        self.configuration.add_creature(min_amount = 1,
                                        max_amount = 1,
                                        name = 'dragon',
                                        location = 'room')
        self.creature_adder = CreatureAdder(self.creature_generator,
                                            self.configuration,
                                            self.rng)

        self.creature_adder.add_creatures(self.level)

    def test_adding_creatures(self):
        """
        Test basic case of adding creatures on the level
        """
        assert_that(self.level.creatures, has_length(greater_than(3)))
        assert_that(self.level.creatures, has_length(less_than(6)))

        assert_that(self.level, has_creature('rat',
                                             greater_than_or_equal_to(3)))
        assert_that(self.level, has_creature('dragon', 1))

    def test_adding_to_location(self):
        """
        Test that CreatureAdder will use location types passed to it
        """
        dragon = [x for x in self.level.creatures
                  if x.name == 'dragon'][0]

        location = dragon.location

        assert_that(located_in_room(dragon))
