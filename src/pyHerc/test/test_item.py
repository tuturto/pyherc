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
from pyHerc.test import IntegrationTest

class test_item_with_generator(IntegrationTest):
    """
    Tests for items that require item generator to be working
    """

    def setUp2(self):
        self.item = None
        self.level = None
        self.dungeon = None
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

        self.model.dungeon = self.dungeon
        self.model.player = self.character

    def test_crystal_skull_generation(self):
        """
        Test that generating crystal skull is possible
        """
        self.item = self.itemGenerator.generateItem(self.tables, {'type': 'special',
                                                'name': 'crystal skull'})

        assert(self.item.name == 'crystal skull')
        assert(self.item.questItem == 1)
        assert(self.item.icon == pyHerc.data.tiles.item_crystal_skull)

    def test_create_weapon(self):
        """
        Test that a weapon can be created
        """

        item = self.itemGenerator.generateItem(self.tables, {'name': 'dagger'})

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

    def test_wield_weapon(self):
        """
        Test that character can wield a weapon (dagger)
        """
        item = self.itemGenerator.generateItem(self.tables, {'name': 'dagger'})

        assert(item not in self.character.weapons)

        pyHerc.rules.items.wield(self.model, self.character, item)

        assert(item in self.character.weapons)

    def test_dual_wielding(self):
        """
        Test that character can swap a weapon to another
        """
        item1 = self.itemGenerator.generateItem(self.tables, {'name': 'dagger'})
        item2 = self.itemGenerator.generateItem(self.tables, {'name': 'sickle'})

        assert(item1 not in self.character.weapons)
        assert(item2 not in self.character.weapons)

        pyHerc.rules.items.wield(self.model, self.character, item1)
        pyHerc.rules.items.wield(self.model, self.character, item2,  dualWield = True)

        assert(item1 in self.character.weapons)
        assert(item2 in self.character.weapons)

    def test_dual_wielding_two_handed_weapons(self):
        """
        Test that character can not dual wield two-handed weapon
        """
        item1 = self.itemGenerator.generateItem(self.tables, {'name': 'longspear'})
        item2 = self.itemGenerator.generateItem(self.tables, {'name': 'sickle'})

        assert(item1 not in self.character.weapons)
        assert(item2 not in self.character.weapons)

        pyHerc.rules.items.wield(self.model, self.character, item2)
        pyHerc.rules.items.wield(self.model, self.character, item1,  dualWield = True)

        assert(item1 not in self.character.weapons)
        assert(item2 in self.character.weapons)

    def test_can_dual_wield(self):
        """
        Test that system can determine if two items can be dual-wielded
        """
        item1 = self.itemGenerator.generateItem(self.tables, {'name': 'longspear'})
        item2 = self.itemGenerator.generateItem(self.tables, {'name': 'sickle'})

        assert(not pyHerc.rules.items.canDualWield(self.model, self.character, item1, item2))

    def test_dual_wieldable(self):
        """
        Test that system can determine if item is dual-wieldable
        """
        item1 = self.itemGenerator.generateItem(self.tables, {'name': 'longspear'})
        item2 = self.itemGenerator.generateItem(self.tables, {'name': 'sickle'})

        assert(not pyHerc.rules.items.dualWieldable(self.model, self.character, item1))
        assert(pyHerc.rules.items.dualWieldable(self.model, self.character, item2))

    def test_dual_wieldable_apples(self):
        """
        Test that system can determine if item is dual-wieldable when using mundane items
        """
        item = self.itemGenerator.generateItem(self.tables, {'name': 'apple'})

        assert(not pyHerc.rules.items.dualWieldable(self.model, self.character, item))

    def test_potion_creation(self):
        """
        Test that basic healing potion can be created
        """
        self.item = self.itemGenerator.generateItem(self.tables, {'name': 'healing potion'})

        assert(self.item != None)
        assert(self.item.charges == 1)
        assert('on drink' in self.item.effects.keys())

        effect = self.item.effects['on drink'][0]
        assert(effect['name'] == 'healing')
        assert(effect['power'] == '1d10')

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

    def test_picking_up(self):
        """
        Test that item can be picked up
        """
        assert(self.character.location == (5, 5))
        assert(self.item.location == (5, 5))

        pyHerc.rules.items.pickUp(self.model, self.character, self.item)

        assert(self.item in self.character.inventory)
        assert(not self.item in self.level.items)
        assert(self.item.location == ())

    def test_picking_up_not_correct_location(self):
        """
        Test that item is not picked up from wrong location
        """
        self.character.location = (6, 6)

        assert(self.character.location == (6, 6))
        assert(self.item.location == (5, 5))

        pyHerc.rules.items.pickUp(self.model, self.character, self.item)

        assert(self.item in self.character.inventory)
        assert(not self.item in self.level.items)

    def test_dropping_item(self):
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

    def test_finding_items(self):
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

class test_ItemAdvanced():
    """
    Testing more advanced features of item class
    """

    def test_appearance_of_unknown(self):
        """"
        Test that appearance is reported for an unknown item
        """

        item = pyHerc.data.model.Item()
        character = pyHerc.data.model.Character()

        item.name = 'healing potion'
        item.appearance = 'blue potion'

        name = item.get_name(character)

        assert(name == 'blue potion')

    def test_appearance_of_generic_named_item(self):
        """
        Test that given name is reported for a generally named item
        """
        item = pyHerc.data.model.Item()
        character = pyHerc.data.model.Character()
        character.itemMemory['healing potion'] = 'doozer potion'

        item.name = 'healing potion'
        item.appearance = 'blue potion'

        name = item.get_name(character)

        assert(name == 'doozer potion')

    def test_identifying_item(self):
        """
        Test that character can identify an item
        """
        item = pyHerc.data.model.Item()
        character = pyHerc.data.model.Character()
        item.name = 'healing potion'
        item.appearance = 'blue potion'

        name = item.get_name(character)
        assert(name == 'blue potion')

        character.identify_item(item)

        name = item.get_name(character)
        assert(name == 'healing potion')

    def test_item_name_decoration(self):
        '''
        Test that item can decorate its name by adding (being worn) or (weapon in hand) to the name
        '''
        item = pyHerc.data.model.Item()
        character = pyHerc.data.model.Character()
        item.name = 'club'

        character.inventory.append(item)
        name = item.get_name(character)
        assert(name == 'club')

        character.weapons = [item]
        name = item.get_name(character)
        assert(name == 'club (weapon in hand)')
