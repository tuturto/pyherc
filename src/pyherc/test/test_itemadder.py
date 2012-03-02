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
Tests for ItemAdder
"""
#pylint: disable=W0614
from pyDoubles.framework import spy, empty_stub, stub #pylint: disable=F0401, E0611
from pyDoubles.framework import assert_that_method #pylint: disable=F0401, E0611
from hamcrest import * #pylint: disable=W0401
from pyherc.test.matchers import located_in_room, does_have_item

from pyherc.data import Level
from pyherc.data.tiles import FLOOR_ROCK
from pyherc.data.tiles import WALL_EMPTY
from pyherc.generators.item import ItemGenerator
from pyherc.generators.level.items import ItemAdder
from pyherc.generators.level.items import ItemAdderConfiguration
from pyherc.rules.tables import Tables
import random

class TestItemAdder():
    """
    Tests for ItemAdder
    """
    def __init__(self):
        """
        Default constructor
        """
        self.rng = None
        self.level = None
        self.mock_tables = None
        self.item_generator = None
        self.configuration = None
        self.item_adder = None

    def setup(self):
        """
        Setup the test case
        """
        self.rng = random.Random()
        self.level = Level((60, 40), FLOOR_ROCK, WALL_EMPTY)
        self.level.set_location_type((10, 10), 'room')

        for x_loc in range(11, 30):
            self.level.set_location_type((x_loc, 10), 'corridor')

        self.mock_tables = stub(Tables)
        self.mock_tables.items = {}
        self.mock_tables.items['dagger'] = {'name': 'dagger',
                                            'icon': 1,
                                            'cost': 5,
                                            'weight': 10,
                                            'rarity': 32,
                                            'type': ['weapon']}

        self.mock_tables.items['red potion'] = {'name': 'red potion',
                                                'icon': 2,
                                                'cost': 500,
                                                'weight': 1,
                                                'rarity': 16,
                                                'type': ['potion']}

        self.mock_tables.tag_score = {'potion': 1}
        self.mock_tables.items_by_tag = {'potion': [('red potion', 0, 1)]}

        self.item_generator = ItemGenerator(self.mock_tables)

        self.configuration = ItemAdderConfiguration(['crypt'])
        self.configuration.add_item(min_amount = 3,
                                    max_amount = 4,
                                    name = 'dagger')
        self.configuration.add_item(min_amount = 1,
                                    max_amount = 1,
                                    type = 'potion',
                                    location = 'room')
        self.item_adder = ItemAdder(self.item_generator,
                                    self.configuration,
                                    self.rng)

        self.item_adder.add_items(self.level)

    def test_adding_items(self):
        """
        Test basic case of adding items on the level
        """
        assert_that(self.level.items, has_length(greater_than(3)))
        assert_that(self.level.items, has_length(less_than(6)))

        assert_that(self.level, does_have_item('dagger',
                                        greater_than_or_equal_to(3)))
        assert_that(self.level, does_have_item('red potion', 1))

    def test_adding_to_location(self):
        """
        Test that ItemAdder will use location types passed to it
        """
        potion = [x for x in self.level.items
                  if x.name == 'red potion'][0]

        location = potion.location

        assert_that(located_in_room(potion))
