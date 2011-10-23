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
import pyHerc.rules.magic
import pyHerc.data.model
from pyHerc.data.item import Item
from pyHerc.data.item import ItemEffectData
from pyHerc.test import IntegrationTest
from pyHerc.test import StubModel

class test_magic:

    def test_damage_effect(self):
        """
        Test that a damage effect can be applied on a character
        """
        model = StubModel()
        character = pyHerc.data.model.Character()
        character.hp = 15
        character.maxHp = 15
        pyHerc.rules.magic.cast_effect(
                            model, character,
                            ItemEffectData('on drink', 'damage', '1d10'), [10])

        assert(character.hp == 5)

    def test_healing_effect(self):
        """
        Test that a healing effect can be applied on a character
        """
        model = StubModel()
        character = pyHerc.data.model.Character()
        character.hp = 1
        character.maxHp = 15
        pyHerc.rules.magic.cast_effect(
                            model, character,
                            ItemEffectData('on drink', 'healing', '1d10'), [10])

        assert(character.hp == 11)

    def test_healing_does_not_heal_over_max_hp(self):
        """
        Test that character does not get healed over his maximum hp when getting healing effect
        """
        model = StubModel()
        character = pyHerc.data.model.Character()
        character.hp = 1
        character.maxHp = 5
        pyHerc.rules.magic.cast_effect(
                        model, character,
                        ItemEffectData('on drink', 'healing', '1d10'), [10])

        assert(character.hp == 5)

class test_magicWithGenerators(IntegrationTest):

    def setUp2(self):
        self.character = pyHerc.data.model.Character()
        self.character.hp = 1
        self.character.maxHp = 5

        self.item = Item()
        self.item.name = 'healing potion'
        self.item.add_effect(ItemEffectData('on drink', 'healing', '1d10', 1))

        self.character.inventory.append(self.item)

    def test_drinking_empty_potion(self):
        """
        Test that empty potion has no effect
        """
        self.item.effects = {}
        pyHerc.rules.items.drink_potion(self.model, self.character, self.item, [10])

        assert(self.character.hp == 1)

    def test_drinking_healing_potion(self):
        """
        Test that character drinking a healing potion gets healed
        """
        pyHerc.rules.items.drink_potion(self.model, self.character, self.item, [10])

        assert(self.character.hp == 5)
        assert(self.item.maximum_charges_left() == 0)

    def test_drinking_potion_identifies_it(self):
        """
        Test that drinking a potion correctly identifies it
        """
        pyHerc.rules.items.drink_potion(self.model, self.character, self.item)

        name = self.item.get_name(self.character)
        assert(name == 'healing potion')

    def test_drinking_potion_empty_discards_it(self):
        """
        Test that empty potion is discarded from character inventory
        """
        assert(self.item in self.character.inventory)
        pyHerc.rules.items.drink_potion(self.model, self.character, self.item)
        assert(not self.item in self.character.inventory)

    def test_drinking_potion_does_not_discard_it(self):
        """
        Test that non-empty potions are not discarded after drinking
        """
        self.item = Item()
        self.item.name = 'healing potion'
        self.item.add_effect(ItemEffectData('on drink', 'healing', '1d10', 5))
        self.character.inventory.append(self.item)

        assert(self.item in self.character.inventory)
        pyHerc.rules.items.drink_potion(self.model, self.character, self.item)
        assert(self.item in self.character.inventory)

    def test_drinking_non_potion(self):
        '''
        Test that drinking non-potion item will not crash the system
        '''
        self.item = Item()
        self.item.name = 'club'
        self.character.inventory.append(self.item)
        pyHerc.rules.items.drink_potion(self.model, self.character, self.item)
