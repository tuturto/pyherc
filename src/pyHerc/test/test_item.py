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
import pyHerc.generators.item
import pyHerc.data.tiles
import pyHerc.data.dungeon
import pyHerc.rules.items
import pyHerc.rules.tables

class test_ItemWithGenerator:
    """
    Tests for items that require item generator to be working
    """

    def setup(self):
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
    <item>
        <name>dagger</name>
        <cost>2</cost>
        <damage>1d4</damage>
        <criticalRange>19</criticalRange>
        <criticalDamage>2</criticalDamage>
        <weight>1</weight>
        <damageTypes>
            <damageType>piercing</damageType>
            <damageType>slashing</damageType>
        </damageTypes>
        <class>simple</class>
        <icons>
            <icon>item_dagger_1</icon>
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
        <name>longspear</name>
        <cost>5</cost>
        <damage>1d8</damage>
        <criticalRange>20</criticalRange>
        <criticalDamage>3</criticalDamage>
        <weight>9</weight>
        <damageTypes>
            <damageType>piercing</damageType>
        </damageTypes>
        <class>simple</class>
        <icons>
            <icon>item_longspear</icon>
        </icons>
        <types>
            <type>weapon</type>
            <type>two-handed weapon</type>
            <type>melee</type>
            <type>simple weapon</type>
        </types>
        <rarity>common</rarity>
    </item>
    <item>
        <name>sickle</name>
        <cost>6</cost>
        <damage>1d6</damage>
        <criticalRange>20</criticalRange>
        <criticalDamage>2</criticalDamage>
        <weight>2</weight>
        <damageTypes>
            <damageType>slashing</damageType>
        </damageTypes>
        <class>simple</class>
        <icons>
            <icon>item_sickle</icon>
        </icons>
        <types>
            <type>weapon</type>
            <type>light weapon</type>
            <type>melee</type>
            <type>simple weapon</type>
        </types>
        <rarity>common</rarity>
    </item>
</items>
"""
        self.item = None
        self.level = None
        self.dungeon = None
        self.model = None
        self.character = None

        self.item = pyHerc.data.model.Item()
        self.item.name = 'banana'
        self.item.location = ()
        self.item.icon = None

        self.level = pyHerc.data.dungeon.Level([20, 20], pyHerc.data.tiles.floor_rock,
                                                    pyHerc.data.tiles.wall_empty)

        self.character = pyHerc.data.model.Character()

        self.character.location = (5, 5)
        self.character.name = 'Timothy Tester'
        self.character.level = self.level
        self.character.speed = 1
        self.character.tick = 1

        self.level.addItem(self.item, (5, 5))

        self.dungeon = pyHerc.data.dungeon.Dungeon()
        self.dungeon.levels = self.level

        self.model = pyHerc.data.model.Model()
        self.model.dungeon = self.dungeon
        self.model.player = self.character

        self.generator = pyHerc.generators.item.ItemGenerator()
        self.tables = pyHerc.rules.tables.Tables()
        self.tables.loadTables(itemConfig)

    def test_crystalSkullGeneration(self):
        """
        Test that generating crystal skull is possible
        """
        self.item = self.generator.generateItem(self.tables, {'type': 'special',
                                                'name': 'crystal skull'})

        assert(self.item.name == 'crystal skull')
        assert(self.item.questItem == 1)
        assert(self.item.icon == pyHerc.data.tiles.item_crystal_skull)

    def test_createWeapon(self):
        """
        Test that a weapon can be created
        """

        item = self.generator.generateItem(self.tables, {'name': 'dagger'})

        assert(item != None)
        assert(item.name == 'dagger')
        assert(item.cost == 2)
        assert(item.damage == '1d4')
        assert(item.criticalRange == 19)
        assert(item.criticalDamage == 2)
        assert(item.weight == 1)
        assert('piercing' in item.damageType)
        assert('slashing' in item.damageType)
        assert(item.weaponType == 'simple')
        assert('weapon' in item.tags)
        assert('simple weapon' in item.tags)
        assert(item.rarity == 32)

    def test_wieldWeapon(self):
        """
        Test that character can wield a weapon (dagger)
        """
        item = self.generator.generateItem(self.tables, {'name': 'dagger'})

        assert(item not in self.character.weapons)

        pyHerc.rules.items.wield(self.model, self.character, item)

        assert(item in self.character.weapons)

    def test_dualWielding(self):
        """
        Test that character can swap a weapon to another
        """
        item1 = self.generator.generateItem(self.tables, {'name': 'dagger'})
        item2 = self.generator.generateItem(self.tables, {'name': 'sickle'})

        assert(item1 not in self.character.weapons)
        assert(item2 not in self.character.weapons)

        pyHerc.rules.items.wield(self.model, self.character, item1)
        pyHerc.rules.items.wield(self.model, self.character, item2,  dualWield = True)

        assert(item1 in self.character.weapons)
        assert(item2 in self.character.weapons)

    def test_dualWieldingTwoHandedWeapons(self):
        """
        Test that character can not dual wield two-handed weapon
        """
        item1 = self.generator.generateItem(self.tables, {'name': 'longspear'})
        item2 = self.generator.generateItem(self.tables, {'name': 'sickle'})

        assert(item1 not in self.character.weapons)
        assert(item2 not in self.character.weapons)

        pyHerc.rules.items.wield(self.model, self.character, item2)
        pyHerc.rules.items.wield(self.model, self.character, item1,  dualWield = True)

        assert(item1 not in self.character.weapons)
        assert(item2 in self.character.weapons)

    def test_canDualWield(self):
        """
        Test that system can determine if two items can be dual-wielded
        """
        item1 = self.generator.generateItem(self.tables, {'name': 'longspear'})
        item2 = self.generator.generateItem(self.tables, {'name': 'sickle'})

        assert(not pyHerc.rules.items.canDualWield(self.model, self.character, item1, item2))

    def test_dualWieldable(self):
        """
        Test that system can determine if item is dual-wieldable
        """
        item1 = self.generator.generateItem(self.tables, {'name': 'longspear'})
        item2 = self.generator.generateItem(self.tables, {'name': 'sickle'})

        assert(not pyHerc.rules.items.dualWieldable(self.model, self.character, item1))
        assert(pyHerc.rules.items.dualWieldable(self.model, self.character, item2))

    def test_dualWieldableApples(self):
        """
        Test that system can determine if item is dual-wieldable when using mundane items
        """
        item = self.generator.generateItem(self.tables, {'name': 'apple'})

        assert(not pyHerc.rules.items.dualWieldable(self.model, self.character, item))


class test_Item:

    def setup(self):
        self.item = None
        self.level = None
        self.dungeon = None
        self.model = None
        self.character = None

        self.item = pyHerc.data.model.Item()
        self.item.name = 'banana'
        self.item.location = ()
        self.item.icon = None

        self.level = pyHerc.data.dungeon.Level([20, 20], pyHerc.data.tiles.floor_rock,
                                                    pyHerc.data.tiles.wall_empty)

        self.character = pyHerc.data.model.Character()

        self.character.location = (5, 5)
        self.character.name = 'Timothy Tester'
        self.character.level = self.level
        self.character.speed = 1
        self.character.tick = 1

        self.level.addItem(self.item, (5, 5))

        self.dungeon = pyHerc.data.dungeon.Dungeon()
        self.dungeon.levels = self.level

        self.model = pyHerc.data.model.Model()
        self.model.dungeon = self.dungeon
        self.model.player = self.character

    def test_pickingUp(self):
        """
        Test that item can be picked up
        """
        assert(self.character.location == (5, 5))
        assert(self.item.location == (5, 5))

        pyHerc.rules.items.pickUp(self.model, self.character, self.item)

        assert(self.item in self.character.inventory)
        assert(not self.item in self.level.items)
        assert(self.item.location == ())

    def test_pickingUpNotCorrectLocation(self):
        """
        Test that item is not picked up from wrong location
        """
        self.character.location = (6, 6)

        assert(self.character.location == (6, 6))
        assert(self.item.location == (5, 5))

        pyHerc.rules.items.pickUp(self.model, self.character, self.item)

        assert(self.item in self.character.inventory)
        assert(not self.item in self.level.items)

    def test_droppingItem(self):
        """
        Test that an item can be dropped from inventory
        """
        pyHerc.rules.items.pickUp(self.model, self.character, self.item)

        assert(self.item in self.character.inventory)
        assert(not self.item in self.level.items)

        self.character.location = (8, 8)
        pyHerc.rules.items.drop(self.model, self.character, self.item)

        assert(not self.item in self.character.inventory)
        assert(self.item in self.level.items)
        assert(self.item.location == (8, 8))

    def test_findingItems(self):
        """
        Test that level can be queried for items on a certain location
        """

        item = pyHerc.data.model.Item()
        item.name = 'apple'
        item.location = ()
        item.icon = None
        self.level.addItem(item, (5, 5))

        item = pyHerc.data.model.Item()
        item.name = 'kiwi'
        item.location = ()
        item.icon = None
        self.level.addItem(item, (3, 3))

        items = self.level.getItemsAt((5, 5))
        assert(len(items) == 2)

        items = self.level.getItemsAt((3, 3))
        assert(len(items) == 1)

        items = self.level.getItemsAt((12, 0))
        assert(len(items) == 0)
