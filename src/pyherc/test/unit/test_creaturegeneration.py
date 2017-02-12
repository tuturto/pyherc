# -*- coding: utf-8 -*-

# Copyright (c) 2010-2017 Tuukka Turto
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
Tests for creature generation
"""

from functools import partial
from random import Random

from hamcrest import assert_that, equal_to, is_, not_none
from mockito import mock, verify
from pyherc.data.effects import DamageModifier, EffectHandle
from pyherc.generators import (creature_config, generate_creature,
                               inventory_config, ItemGenerator,
                               ItemConfiguration, ItemConfigurations)
from pyherc.test.matchers import has_effect, has_effect_handle


class MockAI():
    """
    Simple class to fake an AI class
    """

    def __init__(self, character):
        """
        Default constructor
        """
        pass


class TestCreatureGeneration():
    """
    Tests for creature generator
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.creature_config = None
        self.generator = None

        self.model = None
        self.rng = None

    def setup(self):
        """
        Setup test case
        """
        self.creature_config = {}

        self.model = mock()
        self.rng = Random()

        self.creature_config['rat'] = creature_config(name='rat',
                                                      body=4,
                                                      finesse=12,
                                                      mind=2,
                                                      hp=2,
                                                      speed=2,
                                                      icons=[100, 101],
                                                      attack=2,
                                                      ai=MockAI)

        self.creature_config['spider'] = creature_config(
            name='spider',
            body=6,
            finesse=12,
            mind=8,
            hp=6,
            speed=1,
            icons=[102],
            attack=4,
            ai=MockAI,
            effect_handles=[EffectHandle(trigger='on attack hit',
                                         effect='minor poison',
                                         parameters=None,
                                         charges=100)])

        self.creature_config['skeleton warrior'] = creature_config(
            name='skeleton warrior',
            body=8,
            finesse=11,
            mind=0,
            hp=8,
            speed=2.5,
            icons=[110],
            attack=2,
            ai=MockAI,
            effects=[DamageModifier(modifier=2,
                                    damage_type='crushing',
                                    duration=None,
                                    frequency=None,
                                    tick=None,
                                    icon=101,
                                    title='title',
                                    description='description')])

        self.creatures = partial(generate_creature,
                                 configuration=self.creature_config,
                                 model=self.model,
                                 rng=self.rng,
                                 item_generator=mock())

    def test_creating_simple_creature(self):
        """
        Test that simple creature can be created by name
        """
        creature = self.creatures(name='rat')

        assert_that(creature.name, is_(equal_to('rat')))

    def test_creating_creature_with_effect_handle(self):
        """
        Test that creature with effect handle can be created
        """
        creature = self.creatures(name='spider')

        assert_that(creature, has_effect_handle())

    def test_creating_creature_with_effect(self):
        """
        Test that creature with effect can be created
        """
        creature = self.creatures(name='skeleton warrior')

        assert_that(creature, has_effect())

    def test_creating_creature_with_ai(self):
        """
        Test that creature can have AI created
        """
        creature = self.creatures(name='rat')

        assert_that(creature.artificial_intelligence,
                    is_(not_none()))


class TestItemsInCreatureGeneration():
    """
    Test that items can be handled in creature generation
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

        self.model = None
        self.rng = None
        self.skeleton_config = None
        self.creature_config = None

    def setup(self):
        """
        Setup testcases
        """
        self.model = mock()
        self.rng = Random()

        inventory = [inventory_config('dagger', 1, 1, 100)]

        self.skeleton_config = creature_config(
            name='skeleton warrior',
            body=8,
            finesse=11,
            mind=0,
            hp=8,
            speed=2.5,
            icons=[405],
            attack=2,
            ai=MockAI,
            inventory=inventory)

        self.creature_config = {}

        self.creature_config['skeleton warrior'] = self.skeleton_config

        item_config = ItemConfigurations(self.rng)
        item_config.add_item(ItemConfiguration(name='dagger',
                                               cost=2,
                                               weight=2,
                                               icons='foo',
                                               types=['item'],
                                               rarity='common'))
        items = ItemGenerator(item_config)

        self.creatures = partial(generate_creature,
                                 self.creature_config,
                                 self.model,
                                 items,
                                 self.rng)

    def test_creating_creature_with_item_calls_itemgenerator(self):
        """
        Test that generating creature with item calls item generator
        """
        skeleton = self.creatures('skeleton warrior')

        assert_that(len(skeleton.inventory), is_(equal_to(1)))
