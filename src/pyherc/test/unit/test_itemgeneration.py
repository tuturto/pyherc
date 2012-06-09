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
