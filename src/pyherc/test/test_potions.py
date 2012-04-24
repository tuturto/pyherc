#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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
Module for item effect tests
"""
#pylint: disable=W0614
from pyherc.data import Character
from pyherc.data import Model
from pyherc.data import Item
from pyherc.data import ItemEffectData
from pyherc.rules.consume import DrinkFactory
from pyherc.rules import ActionFactory
from random import Random

from hamcrest import * #pylint: disable=W0401
from mockito import mock

class TestPotions():
    """
    Magic tests with generated items
    """

    def __init__(self):
        """
        Default constructor
        """
        self.character = None
        self.action_factory = None
        self.potion = None
        self.model = None
        self.rng = None

    def setup(self):
        """
        Setup the test case
        """
        self.rng = Random()
        self.model = mock()

        drink_factory = DrinkFactory()
        self.action_factory = ActionFactory(self.model,
                                            drink_factory)

        self.character = Character(self.model,
                                   self.action_factory,
                                   self.rng)
        self.character.hit_points = 1
        self.character.max_hp = 5
        self.character.model = self.model

        self.potion = Item()
        self.potion.name = 'healing potion'
        self.potion.add_effect(ItemEffectData('on drink', 'healing', '1d10', 1))

        self.character.inventory.append(self.potion)

    def test_drinking_empty_potion(self):
        """
        Test that empty potion has no effect
        """
        self.potion.effects = {}
        self.character.drink(self.potion)

        assert_that(self.character.hit_points, is_(equal_to(1)))

    def test_drinking_healing_potion(self):
        """
        Test that character drinking a healing potion gets healed
        """
        self.character.drink(self.potion)

        assert_that(self.character.hit_points, is_(greater_than(1)))
        assert_that(self.potion.maximum_charges_left, is_(equal_to(0)))

    def test_drinking_potion_identifies_it(self):
        """
        Test that drinking a potion correctly identifies it
        """
        self.character.drink(self.potion)

        name = self.potion.get_name(self.character)
        assert_that(name, is_(equal_to('healing potion')))

    def test_drinking_potion_empty_discards_it(self):
        """
        Test that empty potion is discarded from character inventory
        """
        assert_that(self.character.inventory, has_item(self.potion))
        self.character.drink(self.potion)
        assert_that(self.character.inventory, is_not(has_item(self.potion)))

    def test_drinking_potion_does_not_discard_it(self):
        """
        Test that non-empty potions are not discarded after drinking
        """
        self.potion = Item()
        self.potion.name = 'healing potion'
        self.potion.add_effect(ItemEffectData('on drink', 'healing', '1d10', 5))
        self.character.inventory.append(self.potion)

        assert_that(self.character.inventory, has_item(self.potion))
        self.character.drink(self.potion)
        assert_that(self.character.inventory, has_item(self.potion))

    def test_drinking_non_potion(self):
        """
        Test that drinking non-potion item will not crash the system
        """
        item = Item()
        item.name = 'club'
        self.character.inventory.append(self.potion)
        self.character.drink(item)