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
                    <icon>item_apple</icon>
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
        assert tables.items['apple']['rarity'] == 'common'
        assert tables.items['apple']['icon'] == pyHerc.data.tiles.item_apple

    def test_readingMoreComplexItem(self):
        itemConfig = """
            <items>
                <item>
                    <name>crystal skull</name>
                    <cost>0</cost>
                    <weight>5</weight>
                    <questItem>1</questItem>
                    <icon>item_crystal_skull</icon>
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
        assert tables.items['crystal skull']['rarity'] == 'artifact'
        assert tables.items['crystal skull']['icon'] == pyHerc.data.tiles.item_crystal_skull
