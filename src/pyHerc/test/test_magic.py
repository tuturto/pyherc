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
from pyHerc.test import IntegrationTest
from pyHerc.test import StubModel

class test_magic:

    def test_healingEffect(self):
        """
        Test that a healing effect can be applied on a character
        """
        model = StubModel()
        character = pyHerc.data.model.Character()
        character.hp = 1
        character.maxHp = 15
        pyHerc.rules.magic.castEffect(model, character, {'name':'healing', 'power':'1d10'}, [10])

        assert(character.hp == 11)

    def test_healingDoesNotHealOverMaxHP(self):
        """
        Test that character does not get healed over his maximum hp when getting healing effect
        """
        model = StubModel()
        character = pyHerc.data.model.Character()
        character.hp = 1
        character.maxHp = 5
        pyHerc.rules.magic.castEffect(model, character, {'name':'healing', 'power':'1d10'}, [10])

        assert(character.hp == 5)

class test_magicWithGenerators(IntegrationTest):

    def setUp2(self):
        self.character = pyHerc.data.model.Character()
        self.character.hp = 1
        self.character.maxHp = 5

        self.item = pyHerc.data.model.Item()
        self.item.name = 'healing potion'
        self.item.charges = 1
        self.item.effects = {'on drink':
                                    [
                                        {'name':'healing', 'power':'1d10'}
                                    ]
                                }

        self.character.inventory.append(self.item)

    def test_drinkingEmptyPotion(self):
        """
        Test that empty potion has no effect
        """
        self.item.charges = 0
        pyHerc.rules.items.drinkPotion(self.model, self.character, self.item, [10])

        assert(self.character.hp == 1)

    def test_drinkingHealingPotion(self):
        """
        Test that character drinking a healing potion gets healed
        """
        pyHerc.rules.items.drinkPotion(self.model, self.character, self.item, [10])

        assert(self.character.hp == 5)
        assert(self.item.charges == 0)

    def test_drinkingPotionIdentifiesIt(self):
        """
        Test that drinking a potion correctly identifies it
        """
        pyHerc.rules.items.drinkPotion(self.model, self.character, self.item, [10])

        name = self.item.getName(self.character)
        assert(name == 'healing potion')
