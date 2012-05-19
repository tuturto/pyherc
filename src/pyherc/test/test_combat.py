#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
Module for testing combat related rules
"""
#pylint: disable=W0614
import pyherc
from pyherc.data import Character
from pyherc.data import Dungeon
from pyherc.generators.level.testlevel import TestLevelGenerator
from pyherc.test import IntegrationTest
from pyherc.test import StubRandomNumberGenerator

from pyherc.rules.public import AttackParameters
from pyherc.rules.attack.action import AttackAction

from pyherc.test.builders import CharacterBuilder

from mockito import mock, verify, when, any
from hamcrest import * #pylint: disable=W0401

class TestMeleeCombat(IntegrationTest):
    """
    Class for testing melee combat related rules
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestMeleeCombat, self).__init__()
        self.level = None
        self.character1 = None
        self.character2 = None

    def setup2(self):

        self.character1 = (CharacterBuilder()
                                .with_model(self.model)
                                .with_action_factory(self.action_factory)
                                .with_rng(self.rng)
                                .with_speed(1)
                                .with_tick(1)
                                .with_hit_points(10)
                                .with_attack(3)
                                .with_body(5)
                                .build())

        self.character2 = (CharacterBuilder()
                                .with_model(self.model)
                                .with_action_factory(self.action_factory)
                                .with_rng(self.rng)
                                .with_speed(1)
                                .with_tick(1)
                                .with_hit_points(10)
                                .with_attack(3)
                                .with_body(5)
                                .build())

        level_generator = TestLevelGenerator(self.action_factory,
                                             self.creatureGenerator,
                                             self.item_generator)

        self.model.dungeon = Dungeon()
        self.level = level_generator.generate_level(None,
                                                   self.model,
                                                   monster_list = [])

        self.model.dungeon.levels = self.level

        self.level.add_creature(self.character1, (5, 5))
        self.level.add_creature(self.character2, (6, 5))

    def test_get_unarmed_action(self):
        """
        Test that unarmed combat action can be generated
        """
        rng = mock()

        action = self.action_factory.get_action(AttackParameters(
                                                      self.character1,
                                                      3,
                                                      'unarmed',
                                                      rng))

        assert_that(action, is_(instance_of(AttackAction)))
        assert_that(action.attack_type, is_(equal_to('unarmed')))

    def test_unarmed_attack(self):
        """
        Test that unarmed attack will harm opponent
        """
        rng = StubRandomNumberGenerator()
        rng.inject(12, [2, 2, 2, 2, 2, 2, 2])

        self.character1.execute_action(AttackParameters(
                                                self.character1,
                                                3,
                                                'unarmed',
                                                rng))

        assert_that(self.character2.hit_points, is_(less_than(10)))

    def test_events_in_unarmed_combat(self):
        """
        Test that attacking raises events
        """
        character1 = (CharacterBuilder()
                        .with_model(self.model)
                        .with_action_factory(self.action_factory)
                        .with_rng(self.rng)
                        .with_attack(12)
                        .with_speed(1)
                        .with_tick(0)
                        .build())

        self.level.add_creature(character1, (2, 2))

        character2 = mock(Character)
        character2.hit_points = 20
        self.level.add_creature(character2, (2, 3))

        character1.perform_attack(5)

        verify(character2).receive_event(any())

    def test_attack_with_weapon(self):
        """
        Test that attack with a weapon will reduce targets hit points
        """
        rng = StubRandomNumberGenerator()
        rng.inject(12, [2, 2, 2, 2, 2, 2, 2])

        dagger = self.item_generator.generate_item({'name': 'dagger'})

        pyherc.rules.items.wield(self.model, self.character1, dagger)

        self.character1.execute_action(AttackParameters(
                                                self.character1,
                                                3,
                                                'melee',
                                                rng))

        assert_that(self.character2.hit_points, is_(equal_to(8)))
