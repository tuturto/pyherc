#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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

import pyherc
import pyherc.rules.magic
import pyherc.data.model
from pyherc.data.item import Item
from pyherc.data.item import ItemEffectData
from pyherc.test import IntegrationTest
from pyherc.test import StubModel

class TestMagic:

    def __init__(self):
        '''
        Default constructor
        '''
        pass

    def test_damage_effect(self):
        """
        Test that a damage effect can be applied on a character
        """
        model = StubModel()
        character = pyherc.data.model.Character(None)
        character.hit_points = 15
        character.max_hp = 15
        pyherc.rules.magic.cast_effect(
                            model, character,
                            ItemEffectData('on drink', 'damage', '1d10'), [10])

        assert(character.hit_points == 5)

    def test_healing_effect(self):
        """
        Test that a healing effect can be applied on a character
        """
        model = StubModel()
        character = pyherc.data.model.Character(None)
        character.hit_points = 1
        character.max_hp = 15
        pyherc.rules.magic.cast_effect(
                            model, character,
                            ItemEffectData('on drink', 'healing', '1d10'), [10])

        assert(character.hit_points == 11)

    def test_healing_does_not_heal_over_max_hp(self):
        """
        Test that character does not get healed over his maximum hp when getting healing effect
        """
        model = StubModel()
        character = pyherc.data.model.Character(None)
        character.hit_points = 1
        character.max_hp = 5
        pyherc.rules.magic.cast_effect(
                        model, character,
                        ItemEffectData('on drink', 'healing', '1d10'), [10])

        assert(character.hit_points == 5)

class TestMagicWithGenerators(IntegrationTest):

    def __init__(self):
        '''
        Default constructor
        '''
        pass

    def setup2(self):
        self.character = pyherc.data.model.Character(self.action_factory)
        self.character.hit_points = 1
        self.character.max_hp = 5

        self.item = Item()
        self.item.name = 'healing potion'
        self.item.add_effect(ItemEffectData('on drink', 'healing', '1d10', 1))

        self.character.inventory.append(self.item)

    def test_drinking_empty_potion(self):
        """
        Test that empty potion has no effect
        """
        self.item.effects = {}
        pyherc.rules.items.drink_potion(self.model, self.character, self.item, [10])

        assert(self.character.hit_points == 1)

    def test_drinking_healing_potion(self):
        """
        Test that character drinking a healing potion gets healed
        """
        pyherc.rules.items.drink_potion(self.model, self.character, self.item, [10])

        assert(self.character.hit_points == 5)
        assert(self.item.maximum_charges_left() == 0)

    def test_drinking_potion_identifies_it(self):
        """
        Test that drinking a potion correctly identifies it
        """
        pyherc.rules.items.drink_potion(self.model, self.character, self.item)

        name = self.item.get_name(self.character)
        assert(name == 'healing potion')

    def test_drinking_potion_empty_discards_it(self):
        """
        Test that empty potion is discarded from character inventory
        """
        assert(self.item in self.character.inventory)
        pyherc.rules.items.drink_potion(self.model, self.character, self.item)
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
        pyherc.rules.items.drink_potion(self.model, self.character, self.item)
        assert(self.item in self.character.inventory)

    def test_drinking_non_potion(self):
        '''
        Test that drinking non-potion item will not crash the system
        '''
        self.item = Item()
        self.item.name = 'club'
        self.character.inventory.append(self.item)
        pyherc.rules.items.drink_potion(self.model, self.character, self.item)
