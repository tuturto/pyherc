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
                    <icon>501</icon>
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
