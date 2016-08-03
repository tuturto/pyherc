# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Module for item effect tests
"""
from random import Random

from hamcrest import assert_that, equal_to, greater_than, has_item, is_, is_not
from mockito import any, mock, when
from pyherc.generators import get_effect_creator
from pyherc.data.effects import Heal
from pyherc.rules import ActionFactory
from pyherc.ports import drink, set_action_factory
from pyherc.rules.consume import DrinkFactory
from pyherc.test.builders import (CharacterBuilder, EffectHandleBuilder,
                                  HealBuilder, ItemBuilder)


class TestPotions():
    """
    Magic tests with generated items
    """

    def __init__(self):
        """
        Default constructor
        """
        self.character = None
        self.potion = None
        self.model = None
        self.rng = None
        self.effect_factory = None

    def setup(self):
        """
        Setup the test case
        """
        self.rng = Random()
        self.model = mock()

        self.effect_factory = get_effect_creator({'heal':
                                  {'type': Heal,
                                   'duration': 0,
                                   'frequency': 0,
                                   'tick': 0,
                                   'healing': 10,
                                   'icon': 101,
                                   'title': 'title',
                                   'description': 'major heal'}})

        drink_factory = DrinkFactory(self.effect_factory)
        set_action_factory(ActionFactory(self.model,
                                         drink_factory))

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

        self.potion = (ItemBuilder()
                            .with_name('healing potion')
                            .with_effect_handle(
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
        drink(self.character,
              self.potion)

        assert_that(self.character.hit_points, is_(equal_to(1)))

    def test_drinking_healing_potion(self):
        """
        Test that character drinking a healing potion gets healed
        """
        drink(self.character,
              self.potion)

        assert_that(self.character.hit_points, is_(greater_than(1)))
        assert_that(self.potion.maximum_charges_left, is_(equal_to(0)))

    def test_drinking_potion_identifies_it(self):
        """
        Test that drinking a potion correctly identifies it
        """
        drink(self.character,
              self.potion)

        name = self.potion.get_name(self.character)
        assert_that(name, is_(equal_to('healing potion')))

    def test_drinking_potion_empty_discards_it(self):
        """
        Test that empty potion is discarded from character inventory
        """
        assert_that(self.character.inventory, has_item(self.potion))
        drink(self.character,
              self.potion)
        assert_that(self.character.inventory, is_not(has_item(self.potion)))

    def test_drinking_potion_does_not_discard_it(self):
        """
        Test that non-empty potions are not discarded after drinking
        """
        self.potion = (ItemBuilder()
                            .with_name('healing potion')
                            .with_effect_handle(
                                EffectHandleBuilder()
                                    .with_trigger('on drink')
                                    .with_charges(5))
                            .build())

        self.character.inventory.append(self.potion)

        assert_that(self.character.inventory, has_item(self.potion))
        drink(self.character,
              self.potion)
        assert_that(self.character.inventory, has_item(self.potion))

    def test_drinking_non_potion(self):
        """
        Test that drinking non-potion item will not crash the system
        """
        item = (ItemBuilder()
                    .with_name('club')
                    .build())

        self.character.inventory.append(self.potion)
        drink(self.character,
              item)
