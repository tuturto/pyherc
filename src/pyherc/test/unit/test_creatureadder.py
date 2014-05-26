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

import random

from functools import partial
from hamcrest import (assert_that, greater_than, greater_than_or_equal_to,
                      has_length, less_than)
from mockito import mock
from pyherc.generators import creature_config
from pyherc.generators.creature import generate_creature
from pyherc.generators.level.creatures import (CreatureAdder,
                                               CreatureAdderConfiguration)
from pyherc.test.matchers import has_creature, located_in_room
from pyherc.test.builders import LevelBuilder
from pyherc.data import get_characters


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
        self.creatures = None
        self.configuration = None
        self.creature_adder = None

    def setup(self):
        """
        Setup the test case
        """
        self.rng = random.Random()
        self.level = (LevelBuilder()
                        .with_size((60, 40))
                        .build())
        self.level.set_location_type((10, 10), 'room')

        config = {}
        config['rat'] = creature_config(name='rat',
                                        body=4,
                                        finesse=12,
                                        mind=2,
                                        hp=2,
                                        speed=2,
                                        icons=1,
                                        attack=2,
                                        ai=None)

        config['dragon'] = creature_config(name='dragon',
                                           body=4,
                                           finesse=12,
                                           mind=2,
                                           hp=2,
                                           speed=2,
                                           icons=1,
                                           attack=2,
                                           ai=None)

        self.model = mock()
        self.creatures = partial(generate_creature,
                                 config,
                                 self.model,
                                 mock(),
                                 self.rng)

        self.configuration = CreatureAdderConfiguration(['crypt'])
        self.configuration.add_creature(min_amount=3,
                                        max_amount=4,
                                        name='rat')
        self.configuration.add_creature(min_amount=1,
                                        max_amount=1,
                                        name='dragon',
                                        location='room')
        self.creature_adder = CreatureAdder(self.creatures,
                                            self.configuration,
                                            self.rng)

        self.creature_adder.add_creatures(self.level)

    def test_adding_creatures(self):
        """
        Test basic case of adding creatures on the level
        """
        assert_that(list(get_characters(self.level)), has_length(greater_than(3)))
        assert_that(list(get_characters(self.level)), has_length(less_than(6)))

        assert_that(self.level, has_creature('rat',
                                             greater_than_or_equal_to(3)))
        assert_that(self.level, has_creature('dragon', 1))

    def test_adding_to_location(self):
        """
        Test that CreatureAdder will use location types passed to it
        """
        dragon = [x for x in get_characters(self.level)
                  if x.name == 'dragon'][0]

        assert_that(located_in_room(dragon))
