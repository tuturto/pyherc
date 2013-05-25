#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
from pyherc.rules.consume import DrinkFactory
from pyherc.rules import ActionFactory
from random import Random

from pyherc.test.builders import CharacterBuilder
from pyherc.test.builders import ItemBuilder
from pyherc.test.builders import EffectHandleBuilder
from pyherc.test.builders import HealBuilder
from hamcrest import assert_that, is_, equal_to, has_item, is_not, greater_than #pylint: disable-msg=E0611
from mockito import mock, when, any

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
        self.effect_factory = None
        self.dying_rules = None

    def setup(self):
        """
        Setup the test case
        """
        self.rng = Random()
        self.model = mock()
        self.effect_factory = mock()
        self.dying_rules = mock()

        drink_factory = DrinkFactory(self.effect_factory,
                                     self.dying_rules)
        self.action_factory = ActionFactory(self.model,
                                            drink_factory)

        self.character = (CharacterBuilder()
                            .with_hit_points(1)
                            .with_max_hp(5)
                            .build())
        effect = (HealBuilder()
                    .with_duration(0)
                    .with_frequency(0)
                    .with_tick(0)
                    .with_healing(5)
                    .with_target(self.character)
                    .build())

        when(self.effect_factory).create_effect(any(),
                                                target = any()).thenReturn(effect)

        self.potion = (ItemBuilder()
                            .with_name('healing potion')
                            .with_effect(
                                EffectHandleBuilder()
                                    .with_trigger('on drink')
                                    .with_effect('heal'))
                            .build())

        self.character.inventory.append(self.potion)

    def test_drinking_empty_potion(self):
        """
        Test that empty potion has no effect
        """
        self.potion = (ItemBuilder()
                            .with_name('empty potion')
                            .build())
        self.character.drink(self.potion,
                             self.action_factory)

        assert_that(self.character.hit_points, is_(equal_to(1)))

    def test_drinking_healing_potion(self):
        """
        Test that character drinking a healing potion gets healed
        """
        self.character.drink(self.potion,
                             self.action_factory)

        assert_that(self.character.hit_points, is_(greater_than(1)))
        assert_that(self.potion.maximum_charges_left, is_(equal_to(0)))

    def test_drinking_potion_identifies_it(self):
        """
        Test that drinking a potion correctly identifies it
        """
        self.character.drink(self.potion,
                             self.action_factory)

        name = self.potion.get_name(self.character)
        assert_that(name, is_(equal_to('healing potion')))

    def test_drinking_potion_empty_discards_it(self):
        """
        Test that empty potion is discarded from character inventory
        """
        assert_that(self.character.inventory, has_item(self.potion))
        self.character.drink(self.potion,
                             self.action_factory)
        assert_that(self.character.inventory, is_not(has_item(self.potion)))

    def test_drinking_potion_does_not_discard_it(self):
        """
        Test that non-empty potions are not discarded after drinking
        """
        self.potion = (ItemBuilder()
                            .with_name('healing potion')
                            .with_effect(
                                EffectHandleBuilder()
                                    .with_trigger('on drink')
                                    .with_charges(5))
                            .build())

        self.character.inventory.append(self.potion)

        assert_that(self.character.inventory, has_item(self.potion))
        self.character.drink(self.potion,
                             self.action_factory)
        assert_that(self.character.inventory, has_item(self.potion))

    def test_drinking_non_potion(self):
        """
        Test that drinking non-potion item will not crash the system
        """
        item = (ItemBuilder()
                    .with_name('club')
                    .build())

        self.character.inventory.append(self.potion)
        self.character.drink(item,
                             self.action_factory)
