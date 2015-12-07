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
Tests for item generation
"""
#pylint: disable=W0614
from random import Random

from hamcrest import assert_that, equal_to, is_, not_none
from pyherc.data.effects import EffectHandle
from pyherc.generators import (ItemConfiguration, ItemConfigurations,
                               ItemGenerator, WeaponConfiguration,
                               TrapConfiguration)
from pyherc.test.matchers import has_damage, has_effect_handle


class TestItemGeneration():
    """
    Tests for new item generator
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestItemGeneration, self).__init__()
        self.item_config = None
        self.generator = None

    def setup(self):
        """
        Setup test case
        """
        self.item_config = ItemConfigurations(Random())

        self.item_config.add_item(
                    ItemConfiguration(name = 'apple',
                                      cost = 1,
                                      weight = 1,
                                      icons = [500, 501],
                                      types = ['food'],
                                      rarity = 'common'))

        self.item_config.add_item(
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
                                            damage = [(2, 'piercing')],
                                            critical_range = 11,
                                            critical_damage = 2,
                                            weapon_class = 'simple')))

        self.item_config.add_item(
                    ItemConfiguration(name = 'healing potion',
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

        self.item_config.add_item(
            ItemConfiguration(name = 'bag of caltrops',
                              cost = 150,
                              weight = 1,
                              icons = ['icon'],
                              types = ['trap bag'],
                              rarity = 'common',
                              trap_configuration = TrapConfiguration(name = 'caltrops',
                                                                     count = 2)))

        self.generator = ItemGenerator(self.item_config)

    def test_create_mundane_item(self):
        """
        Test that creating a simple item is possible
        """
        item = self.generator.generate_item(name = 'apple')

        assert_that(item.name, is_(equal_to('apple')))

    def test_create_weapon(self):
        """
        Test that a weapon can be created
        """
        item = self.generator.generate_item(name = 'dagger')

        weapon_data = item.weapon_data

        assert_that(item, has_damage(2, 'piercing'))

    def test_create_trap_bag(self):
        """
        Test that trap bag can be created
        """
        item = self.generator.generate_item(name = 'bag of caltrops')
        trap_data = item.trap_data

        assert_that(trap_data.trap_name, is_(equal_to('caltrops')))
        assert_that(trap_data.count, is_(equal_to(2)))

    def test_configuring_item_generation(self):
        """
        Test that configuration can be added
        """
        specs = [x for x in self.item_config.get_all_items()
                 if x.name == 'apple']

        assert_that(len(specs), is_(equal_to(1)))

    def test_generate_item_with_effect(self):
        """
        Test that item with effect can be generated
        """
        item = self.generator.generate_item(name = 'healing potion')

        assert_that(item, is_(not_none()))

        assert_that(item, has_effect_handle())

    def test_generating_random_item(self):
        """
        Test that a random item can be generated
        """
        item = self.generator.generate_item(item_type = 'food')

        assert_that(item.name, is_(equal_to('apple')))
