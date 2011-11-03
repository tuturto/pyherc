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

'''
Module for classes testing Item related operations
'''

import pyHerc
import pyHerc.generators.item
import pyHerc.data.tiles
import pyHerc.data.dungeon
import pyHerc.rules.items
import pyHerc.rules.tables
from pyHerc.test import IntegrationTest
from pyHerc.data.item import Item
from pyHerc.data.item import ItemEffectData

class TestItemWithGenerator(IntegrationTest):
    """
    Tests for items that require item generator to be working
    """

    def setUp2(self):
        self.item = None
        self.level = None
        self.dungeon = None
        self.character = None

        self.item = Item()
        self.item.name = 'banana'
        self.item.location = ()
        self.item.icon = None

        self.level = pyHerc.data.dungeon.Level([20, 20],
                                                pyHerc.data.tiles.FLOOR_ROCK,
                                                pyHerc.data.tiles.WALL_EMPTY)

        self.character = pyHerc.data.model.Character()

        self.character.location = (5, 5)
        self.character.name = 'Timothy Tester'
        self.character.level = self.level
        self.character.speed = 1
        self.character.tick = 1

        self.level.add_item(self.item, (5, 5))

        self.dungeon = pyHerc.data.dungeon.Dungeon()
        self.dungeon.levels = self.level

        self.model.dungeon = self.dungeon
        self.model.player = self.character

    def test_crystal_skull_generation(self):
        """
        Test that generating crystal skull is possible
        """
        self.item = self.itemGenerator.generateItem(self.tables,
                                                    {'type': 'special',
                                                    'name': 'crystal skull'})

        assert(self.item.name == 'crystal skull')
        assert(self.item.quest_item == 1)
        assert(self.item.icon == pyHerc.data.tiles.item_crystal_skull)

    def test_create_weapon(self):
        """
        Test that a weapon can be created
        """

        item = self.itemGenerator.generateItem(self.tables, {'name': 'dagger'})

        assert(item != None)
        assert(item.name == 'dagger')
        assert(item.cost == 2)
        assert(item.weapon_data.damage == '1d4')
        assert(item.weapon_data.critical_range == 19)
        assert(item.weapon_data.critical_damage == 2)
        assert(item.weight == 1)
        assert('piercing' in item.weapon_data.damage_type)
        assert('slashing' in item.weapon_data.damage_type)
        assert(item.weapon_data.weapon_type == 'simple')
        assert('weapon' in item.weapon_data.tags)
        assert('simple weapon' in item.weapon_data.tags)
        assert(item.rarity == 32)

    def test_wield_weapon(self):
        """
        Test that character can wield a weapon (dagger)
        """
        item = self.itemGenerator.generateItem(self.tables, {'name': 'dagger'})

        assert(item not in self.character.weapons)

        pyHerc.rules.items.wield(self.model, self.character, item)

        assert(item in self.character.weapons)

    def test_unwielding_item(self):
        '''
        Test that wielded item can be unwielded
        '''
        item = self.itemGenerator.generateItem(self.tables, {'name': 'dagger'})
        pyHerc.rules.items.wield(self.model, self.character, item)

        assert(item in self.character.weapons)

        pyHerc.rules.items.unwield(self.model, self.character, item)

        assert(not item in self.character.weapons)

    def test_dual_wielding(self):
        """
        Test that character can swap a weapon to another
        """
        item1 = self.itemGenerator.generateItem(
                                        self.tables, {'name': 'dagger'})
        item2 = self.itemGenerator.generateItem(
                                        self.tables, {'name': 'sickle'})

        assert(item1 not in self.character.weapons)
        assert(item2 not in self.character.weapons)

        pyHerc.rules.items.wield(self.model, self.character, item1)
        pyHerc.rules.items.wield(self.model,
                                 self.character,
                                 item2,
                                 dualWield = True)

        assert(item1 in self.character.weapons)
        assert(item2 in self.character.weapons)

    def test_dual_wielding_two_handed_weapons(self):
        """
        Test that character can not dual wield two-handed weapon
        """
        item1 = self.itemGenerator.generateItem(self.tables,
                                                {'name': 'longspear'})
        item2 = self.itemGenerator.generateItem(self.tables,
                                                {'name': 'sickle'})

        assert(item1 not in self.character.weapons)
        assert(item2 not in self.character.weapons)

        pyHerc.rules.items.wield(self.model, self.character, item2)
        pyHerc.rules.items.wield(self.model, self.character,
                                 item1,
                                 dualWield = True)

        assert(item1 not in self.character.weapons)
        assert(item2 in self.character.weapons)

    def test_can_dual_wield(self):
        """
        Test that system can determine if two items can be dual-wielded
        """
        item1 = self.itemGenerator.generateItem(self.tables,
                                                {'name': 'longspear'})
        item2 = self.itemGenerator.generateItem(self.tables,
                                                {'name': 'sickle'})

        assert(not pyHerc.rules.items.can_dual_wield(
                                                     self.model,
                                                     self.character,
                                                     item1,
                                                     item2))

    def test_dual_wieldable(self):
        """
        Test that system can determine if item is dual-wieldable
        """
        item1 = self.itemGenerator.generateItem(self.tables,
                                                    {'name': 'longspear'})
        item2 = self.itemGenerator.generateItem(self.tables,
                                                    {'name': 'sickle'})

        assert(not pyHerc.rules.items.is_dual_wieldable(
                                                        self.model,
                                                        self.character,
                                                        item1))
        assert(pyHerc.rules.items.is_dual_wieldable(
                                                    self.model,
                                                    self.character,
                                                    item2))

    def test_dual_wieldable_apples(self):
        """
        Test determing if item is dual-wieldable when using mundane items
        """
        item = self.itemGenerator.generateItem(self.tables,
                                               {'name': 'apple'})

        assert(not pyHerc.rules.items.is_dual_wieldable(
                                                        self.model,
                                                        self.character,
                                                        item))

    def test_potion_creation(self):
        """
        Test that basic healing potion can be created
        """
        self.item = self.itemGenerator.generateItem(self.tables,
                                                    {'name': 'healing potion'})

        assert(self.item != None)
        assert(self.item.charges == 1)
        assert('on drink' in self.item.effects.keys())

        effect = self.item.effects['on drink'][0]
        assert(effect.effect_type == 'healing')
        assert(effect.power == '1d10')

class TestItemsInLevel:
    '''
    Tests performed with items that are placed on levels
    '''

    def setup(self):
        self.item = None
        self.level = None
        self.dungeon = None
        self.model = None
        self.character = None

        self.item = Item()
        self.item.name = 'banana'
        self.item.location = ()
        self.item.icon = None

        self.level = pyHerc.data.dungeon.Level([20, 20],
                                                pyHerc.data.tiles.FLOOR_ROCK,
                                                pyHerc.data.tiles.WALL_EMPTY)

        self.character = pyHerc.data.model.Character()

        self.character.location = (5, 5)
        self.character.name = 'Timothy Tester'
        self.character.level = self.level
        self.character.speed = 1
        self.character.tick = 1

        self.level.add_item(self.item, (5, 5))

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

        pyHerc.rules.items.pick_up(self.model, self.character, self.item)

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

        pyHerc.rules.items.pick_up(self.model, self.character, self.item)

        assert(self.item in self.character.inventory)
        assert(not self.item in self.level.items)

    def test_dropping_item(self):
        """
        Test that an item can be dropped from inventory
        """
        pyHerc.rules.items.pick_up(self.model, self.character, self.item)

        assert(self.item in self.character.inventory)
        assert(not self.item in self.level.items)

        self.character.location = (8, 8)
        pyHerc.rules.items.drop(self.model, self.character, self.item)

        assert(not self.item in self.character.inventory)
        assert(self.item in self.level.items)
        assert(self.item.location == (8, 8))

    def test_dropping_wielded_item(self):
        '''
        Test that wielded item is dropped correctly
        '''
        pyHerc.rules.items.pick_up(self.model, self.character, self.item)
        pyHerc.rules.items.wield(self.model, self.character, self.item)

        assert(self.item in self.character.inventory)
        assert(not self.item in self.level.items)
        assert(self.item in self.character.weapons)

        self.character.location = (8, 8)
        pyHerc.rules.items.drop(self.model, self.character, self.item)

        assert(not self.item in self.character.inventory)
        assert(self.item in self.level.items)
        assert(self.item.location == (8, 8))
        assert(not self.item in self.character.weapons)

    def test_finding_items(self):
        """
        Test that level can be queried for items on a certain location
        """

        item = Item()
        item.name = 'apple'
        item.location = ()
        item.icon = None
        self.level.add_item(item, (5, 5))

        item = Item()
        item.name = 'kiwi'
        item.location = ()
        item.icon = None
        self.level.add_item(item, (3, 3))

        items = self.level.get_items_at((5, 5))
        assert(len(items) == 2)

        items = self.level.get_items_at((3, 3))
        assert(len(items) == 1)

        items = self.level.get_items_at((12, 0))
        assert(len(items) == 0)

class TestItemAdvanced():
    """
    Testing more advanced features of item class
    """

    def test_appearance_of_unknown(self):
        """"
        Test that appearance is reported for an unknown item
        """

        item = Item()
        character = pyHerc.data.model.Character()

        item.name = 'healing potion'
        item.appearance = 'blue potion'

        name = item.get_name(character)

        assert(name == 'blue potion')

    def test_appearance_of_generic_named_item(self):
        """
        Test that given name is reported for a generally named item
        """
        item = Item()
        character = pyHerc.data.model.Character()
        character.item_memory['healing potion'] = 'doozer potion'

        item.name = 'healing potion'
        item.appearance = 'blue potion'

        name = item.get_name(character)

        assert(name == 'doozer potion')

    def test_identifying_item(self):
        """
        Test that character can identify an item
        """
        item = Item()
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
        Test that item can decorate its name
        '''
        item = Item()
        character = pyHerc.data.model.Character()
        item.name = 'club'

        character.inventory.append(item)
        name = item.get_name(character)
        assert(name == 'club')

        character.weapons = [item]
        name = item.get_name(character, True)
        assert(name == 'club (weapon in hand)')

        name = item.get_name(character, False)
        assert(name == 'club')

class TestItemEffects:
    '''
    Tests related to effects on items
    '''

    def setup(self):
        '''
        Set up the test with an item and two effects
        '''

        self.item = Item()

        self.effect1 = ItemEffectData('on drink', 'heal', '1d6')
        self.effect2 = ItemEffectData('on break', 'add charisma', '1')

        self.item.add_effect(self.effect1)
        self.item.add_effect(self.effect2)

    def test_get_all_effects(self):
        '''
        Test that all effects can be returned
        '''

        effects = self.item.get_effects()

        assert(self.effect1 in effects)
        assert(self.effect2 in effects)
        assert(len(effects) == 2)

    def test_get_effects_by_trigger(self):
        '''
        Test that effects triggered by certain trigger can be returned
        '''

        effects = self.item.get_effects('on break')
        assert(not self.effect1 in effects)
        assert(self.effect2 in effects)
        assert(len(effects) == 1)

    def test_get_nonexistent_effect(self):
        '''
        Test that items without effects don't crash effects returning
        '''

        effects = self.item.get_effects('on hit')
        assert(effects == [])

    def test_get_multiple_effects_by_type(self):
        '''
        Test that multiple effects can be returned by type
        '''

        effect3 = ItemEffectData('on break', 'heal', '2d6')
        self.item.add_effect(effect3)

        effects = self.item.get_effects('on break')
        assert(self.effect2 in effects)
        assert(effect3 in effects)
        assert(len(effects) == 2)

class TestItemCharges:
    '''
    Test charge handling of items
    '''

    def setup(self):
        '''
        Set up the test with an item and two effects
        '''

        self.item = Item()

        self.effect1 = ItemEffectData('on drink', 'heal', '1d6')

        self.item.add_effect(self.effect1)

    def test_get_single_charge(self):
        '''
        Test that amount of charges left can be retrieved
        '''
        charges = self.item.charges_left()

        assert(charges == 1)

    def test_multiple_charges(self):
        '''
        Test that amount of charges can be retrieved with multiple effects
        '''
        effect2 = ItemEffectData('on kick', 'damage', '5d10', 2)
        self.item.add_effect(effect2)

        charges = self.item.charges_left()

        assert(len(charges) == 2)
        assert(1 in charges)
        assert(2 in charges)

    def test_extremes_with_multiple_charges(self):
        '''
        Test that smallest and biggest amount of charges left can be retrieved
        '''
        effect2 = ItemEffectData('on kick', 'damage', '5d10', 2)
        self.item.add_effect(effect2)

        minimum_charges = self.item.minimum_charges_left()
        assert(minimum_charges == 1)

        maximum_charges = self.item.maximum_charges_left()
        assert(maximum_charges == 2)
