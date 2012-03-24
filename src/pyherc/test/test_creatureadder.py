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
Tests for CreatureAdder
"""
#pylint: disable=W0614
from pyDoubles.framework import spy, empty_stub, stub #pylint: disable=F0401, E0611
from pyDoubles.framework import assert_that_method #pylint: disable=F0401, E0611
from hamcrest import * #pylint: disable=W0401
from pyherc.test.matchers import has_creature, located_in_room

from pyherc.data import Level
from pyherc.data.tiles import FLOOR_ROCK
from pyherc.data.tiles import WALL_EMPTY
from pyherc.generators.creature import CreatureGenerator
from pyherc.generators.level.creatures import CreatureAdder
from pyherc.generators.level.creatures import CreatureAdderConfiguration
from pyherc.rules.tables import Tables
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
        self.mock_tables = None
        self.mock_action_factory = None
        self.creature_generator = None
        self.configuration = None
        self.creature_adder = None

    def setup(self):
        """
        Setup the test case
        """
        self.rng = random.Random()
        self.level = Level((60, 40), FLOOR_ROCK, WALL_EMPTY)
        self.level.set_location_type((10, 10), 'room')

        self.mock_tables = stub(Tables)
        self.mock_tables.creatures = {}
        self.mock_tables.creatures['rat'] = {'name': 'rat',
                                        'body': 1,
                                        'finesse': 1,
                                        'mind': 1,
                                        'hp': 2,
                                        'speed': 10,
                                        'size': 2,
                                        'attack': 2,
                                        'icon': 1}

        self.mock_tables.creatures['dragon'] = {'name': 'dragon',
                                        'body': 10,
                                        'finesse': 10,
                                        'mind': 10,
                                        'hp': 200,
                                        'speed': 4,
                                        'size': 6,
                                        'attack': 20,
                                        'icon': 2}

        self.mock_action_factory = empty_stub()
        self.model = empty_stub()
        self.creature_generator = CreatureGenerator(self.model,
                                                    self.mock_action_factory,
                                                    self.mock_tables,
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
