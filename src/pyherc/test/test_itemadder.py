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
from pyherc.test.matchers import located_in_room

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

        self.mock_tables = stub(Tables)
        self.mock_tables.items = {}
        self.mock_tables.items['dagger'] = {'name': 'dagger'}

        self.mock_tables.items['red potion'] = {'name': 'red potion'}

        self.item_generator = ItemGenerator(self.mock_tables)

        self.configuration = ItemAdderConfiguration()
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

        assert_that(self.level, has_item('dagger',
                                        greater_than_or_equal_to(3)))
        assert_that(self.level, has_item('potion', 1))

