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
Tests for ItemAdder
"""
from random import Random

from hamcrest import (assert_that,
                      greater_than, greater_than_or_equal_to, has_length,
                      less_than)
from pyherc.data import Model, get_items, add_location_tag
from pyherc.data.effects import EffectHandle
from pyherc.generators.item import (ItemConfiguration, ItemConfigurations,
                                    ItemGenerator, WeaponConfiguration)
from pyherc.generators.level import ItemAdder, ItemAdderConfiguration
from pyherc.test.matchers import does_have_item, located_in_room
from pyherc.test.builders import LevelBuilder


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
        self.item_generator = None
        self.configuration = None
        self.item_adder = None
        self.floor_rock = None
        self.wall_empty = None

    def setup(self):
        """
        Setup the test case
        """
        self.floor_rock = 1
        self.wall_empty = None
        self.rng = Random()
        self.level = (LevelBuilder()
                      .with_size((60, 40))
                      .with_floor_tile(self.floor_rock)
                      .with_wall_tile(self.wall_empty)
                      .build())
        add_location_tag(self.level, (10, 10), 'room')

        for x_loc in range(11, 30):
            add_location_tag(self.level, (x_loc, 10), 'corridor')

        item_config = ItemConfigurations(Random())

        item_config.add_item(
                    ItemConfiguration(name = 'dagger',
                                      cost = 2,
                                      weight = 1,
                                      icons = [500],
                                      types = ['weapon',
                                               'light weapon',
                                               'melee',
                                               'simple weapon'],
                                      rarity = 'common',
                                      weapon_configration = WeaponConfiguration(
                                            damage = [(2, 'piercing'),
                                                      (2, 'slashing')],
                                            critical_range = 11,
                                            critical_damage = 2,
                                            weapon_class = 'simple')))

        item_config.add_item(
                    ItemConfiguration(name = 'red potion',
                                      cost = 150,
                                      weight = 1,
                                      icons = [100],
                                      types = ['potion'],
                                      rarity = 'rare',
                                      effect_handles = [EffectHandle(
                                            trigger = 'on drink',
                                            effect = 'cure medium wounds',
                                            parameters = None,
                                            charges = 1)]))

        self.item_generator = ItemGenerator(item_config)

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
        assert_that(list(get_items(self.level)), has_length(greater_than(3)))
        assert_that(list(get_items(self.level)), has_length(less_than(6)))

        assert_that(self.level, does_have_item('dagger',
                                               greater_than_or_equal_to(3)))
        assert_that(self.level, does_have_item('red potion', 1))

    def test_adding_to_location(self):
        """
        Test that ItemAdder will use location types passed to it
        """
        potion = [x for x in get_items(self.level)
                  if x.name == 'red potion'][0]

        location = potion.location

        assert_that(located_in_room(potion))
