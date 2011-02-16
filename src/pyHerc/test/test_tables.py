#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
#
#   This file is part of pyHerc.
#
#   pyHerc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyHerc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyHerc.  If not, see <http://www.gnu.org/licenses/>.

import pyHerc

class test_Tables:

    def test_readingSimpleItemConfig(self):
        itemConfig = """
            <items>
                <item>
                    <name>apple</name>
                    <cost>1</cost>
                    <weight>1</weight>
                    <icons>
                        <icon>item_apple</icon>
                    </icons>
                    <types>
                        <type>food</type>
                    </types>
                    <rarity>common</rarity>
                </item>
            </items>
            """
        tables = pyHerc.rules.tables.Tables()
        tables.readItemsFromXML(itemConfig)

        assert len(tables.items) == 1
        assert 'apple' in tables.items.keys()
        assert tables.items['apple']['cost'] == 1
        assert tables.items['apple']['weight'] == 1
        assert tables.items['apple']['type'] == ['food']
        assert tables.items['apple']['rarity'] == tables.common
        assert pyHerc.data.tiles.item_apple in tables.items['apple']['icon']

    def test_readingMoreComplexItem(self):
        itemConfig = """
            <items>
                <item>
                    <name>crystal skull</name>
                    <cost>0</cost>
                    <weight>5</weight>
                    <questItem>1</questItem>
                    <icons>
                        <icon>item_crystal_skull</icon>
                    </icons>
                    <types>
                        <type>special item</type>
                        <type>quest item</type>
                    </types>
                    <rarity>artifact</rarity>
                </item>
            </items>
        """
        tables = pyHerc.rules.tables.Tables()
        tables.readItemsFromXML(itemConfig)

        assert len(tables.items) == 1
        assert 'crystal skull' in tables.items.keys()
        assert tables.items['crystal skull']['cost'] == 0
        assert tables.items['crystal skull']['weight'] == 5
        assert tables.items['crystal skull']['questItem'] == 1
        assert 'special item' in tables.items['crystal skull']['type']
        assert 'quest item' in tables.items['crystal skull']['type']
        assert tables.items['crystal skull']['rarity'] == tables.artifact
        assert pyHerc.data.tiles.item_crystal_skull in tables.items['crystal skull']['icon']

    def test_readingTwoItemsFromConfig(self):
        itemConfig = """
            <items>
                <item>
                    <name>apple</name>
                    <cost>1</cost>
                    <weight>1</weight>
                    <icons>
                        <icon>item_apple</icon>
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
                        <icon>item_crystal_skull</icon>
                    </icons>
                    <types>
                        <type>special item</type>
                        <type>quest item</type>
                    </types>
                    <rarity>artifact</rarity>
                </item>
            </items>
        """

        tables = pyHerc.rules.tables.Tables()
        tables.readItemsFromXML(itemConfig)

        assert 'crystal skull' in tables.items.keys()
        assert 'apple' in tables.items.keys()
        assert tables.items['crystal skull']['weight'] == 5
        assert pyHerc.data.tiles.item_apple in tables.items['apple']['icon']

    def test_readingWeaponFromConfig(self):
        itemConfig = """
            <items>
                <item>
                    <name>morning star</name>
                    <cost>8</cost>
                    <damage>1d8</damage>
                    <criticalRange>20</criticalRange>
                    <criticalDamage>2</criticalDamage>
                    <weight>5</weight>
                    <damageTypes>
                        <damageType>bludgeoning</damageType>
                        <damageType>piercing</damageType>
                    </damageTypes>
                    <class>simple</class>
                    <icons>
                        <icon>item_morning_star_1</icon>
                        <icon>item_morning_star_2</icon>
                    </icons>
                    <types>
                        <type>weapon</type>
                        <type>one-handed weapon</type>
                        <type>melee</type>
                        <type>simple weapon</type>
                    </types>
                    <rarity>common</rarity>
                </item>
            </items>
            """
        tables = pyHerc.rules.tables.Tables()
        tables.readItemsFromXML(itemConfig)

        item = tables.items['morning star']
        assert item['name'] == 'morning star'
        assert item['cost'] == 8
        assert item['damage'] == '1d8'
        assert item['critical range'] == 20
        assert item['critical damage'] == 2
        assert item['weight'] == 5
        assert 'bludgeoning' in item['damage type']
        assert 'piercing' in item['damage type']
        assert item['class'] == 'simple'
        assert pyHerc.data.tiles.item_morning_star_1 in item['icon']
        assert pyHerc.data.tiles.item_morning_star_2 in item['icon']
        assert 'weapon' in item['type']
        assert 'one-handed weapon' in item['type']
        assert 'melee' in item['type']
        assert 'simple weapon' in item['type']
        assert item['rarity'] == tables.common
