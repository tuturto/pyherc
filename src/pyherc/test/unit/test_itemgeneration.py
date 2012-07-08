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
from pyherc.rules.tables import Tables
from pyherc.test.matchers import has_effect_handle
from hamcrest import * #pylint: disable=W0401

from pyherc.generators.item import NewItemGenerator, ItemConfigurations
from pyherc.generators.item import ItemConfiguration, WeaponConfiguration
from pyherc.rules.effects import EffectHandle

class TestNewItemGeneration(object):
    """
    Tests for new item generator
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestNewItemGeneration, self).__init__()
        self.item_config = None
        self.generator = None

    def setup(self):
        """
        Setup test case
        """
        self.item_config = ItemConfigurations()

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
                                            damage = 2,
                                            critical_range = 11,
                                            critical_damage = 2,
                                            damage_types = ['piercing',
                                                            'slashing'],
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

        self.generator = NewItemGenerator(self.item_config)

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

        assert_that(weapon_data.damage, is_(equal_to(2)))

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

class TestItemGeneration(object):
    """
    Tests for generating items
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestItemGeneration, self).__init__()
        self.generator = None

    def setup(self):
        """
        Setup the test case
        """
        item_config = itemConfig = """
<items>
    <item>
        <name>apple</name>
        <cost>1</cost>
        <weight>1</weight>
        <icons>
            <icon>ITEM_APPLE</icon>
        </icons>
        <types>
            <type>food</type>
        </types>
        <rarity>common</rarity>
    </item>
    <item>
        <name>crystal skull</name>
        <cost>0</cost>
        <weight>5</weight>
        <questItem>1</questItem>
        <icons>
            <icon>ITEM_CRYSTAL_SKULL</icon>
        </icons>
        <types>
            <type>special item</type>
            <type>quest item</type>
        </types>
        <rarity>artifact</rarity>
    </item>
    <item>
        <name>dagger</name>
        <cost>2</cost>
        <damage>2</damage>
        <criticalRange>11</criticalRange>
        <criticalDamage>2</criticalDamage>
        <weight>1</weight>
        <damageTypes>
            <damageType>piercing</damageType>
            <damageType>slashing</damageType>
        </damageTypes>
        <class>simple</class>
        <icons>
            <icon>ITEM_DAGGER_1</icon>
        </icons>
        <types>
            <type>weapon</type>
            <type>light weapon</type>
            <type>melee</type>
            <type>simple weapon</type>
        </types>
        <rarity>common</rarity>
    </item>
    <item>
        <name>healing potion</name>
        <cost>150</cost>
        <weight>1</weight>
        <charges>1</charges>
        <effects>
                <effect type="on drink" name="cure medium wounds" />
        </effects>
        <icons>
                <icon>ITEM_POTION_1</icon>
        </icons>
        <types>
                <type>potion</type>
        </types>
        <rarity>uncommon</rarity>
    </item>
</items>
"""
        creature_config = """
<creatures>
    <creature>
        <name>rat</name>
        <body>4</body>
        <finesse>12</finesse>
        <mind>2</mind>
        <hp>2</hp>
        <speed>2</speed>
        <icons>
            <icon>CREATURE_RAT_1</icon>
            <icon>CREATURE_RAT_2</icon>
            <icon>CREATURE_RAT_3</icon>
            <icon>CREATURE_RAT_4</icon>
        </icons>
        <attack>2</attack>
        <size>small</size>
    </creature>
</creatures>
"""

        tables = Tables()
        tables.load_tables(None, item_config, creature_config)
        self.generator = ItemGenerator(tables)

    def test_generate_item(self):
        """
        Test that generating simple item is possible
        """
        item = self.generator.generate_item({'name': 'apple'})

        assert_that(item, is_(not_none()))

    def test_generate_item_with_effect(self):
        """
        Test that generating item with effects works
        """
        item = self.generator.generate_item({'name': 'healing potion'})

        assert_that(item, is_(not_none()))

        assert_that(item, has_effect_handle())
