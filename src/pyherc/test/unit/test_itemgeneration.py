#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
Tests for item generation
"""
#pylint: disable=W0614
from pyherc.generators import ItemGenerator
from pyherc.test.matchers import has_effect_handle, has_damage
from hamcrest import * #pylint: disable=W0401

from pyherc.generators import ItemConfigurations
from pyherc.generators import ItemConfiguration, WeaponConfiguration
from pyherc.data.effects import EffectHandle
from random import Random

class TestItemGeneration(object):
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

    def test_configuring_item_generation(self):
        """
        Test that configuration can be added
        """
        apple_spec = filter(lambda x: x.name == 'apple',
                            self.item_config.get_all_items())

        assert_that(len(apple_spec), is_(equal_to(1)))

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
