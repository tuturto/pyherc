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
#from pyherc.generators.level import ItemAdder, item_by_name, item_by_type
from pyherc.test.matchers import does_have_item, located_in_room
from pyherc.test.builders import LevelBuilder

#TODO: enable later
class ItemAdder():
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

        self.configuration = [item_by_name(3, 4, 'dagger'),
                              item_by_type(1, 1, 'potion')]

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
