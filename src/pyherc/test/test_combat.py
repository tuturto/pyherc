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

"""
Module for testing combat related rules
"""

import pyherc
from pyherc.data.dungeon import Dungeon
from pyherc.data.model import Character
from pyherc.generators.level.testlevel import TestLevelGenerator
from pyherc.test import IntegrationTest
from pyherc.test import StubRandomNumberGenerator

from pyherc.rules.public import AttackParameters
from pyherc.rules.attack.action import AttackAction

from mockito import mock, verify, when, any

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
        self.character1 = Character(self.model,
                                    self.action_factory,
                                    self.rng)
        self.character2 = Character(self.model,
                                    self.action_factory,
                                    self.rng)
        level_generator = TestLevelGenerator(self.action_factory,
                                             self.creatureGenerator,
                                             self.item_generator)

        self.model.dungeon = Dungeon()
        self.level = level_generator.generate_level(None,
                                                   self.model,
                                                   monster_list = [])

        self.model.dungeon.levels = self.level

        self.character1.speed = 1
        self.character1.tick = 1
        self.character1.hit_points = 10
        self.character1.attack = 3
        self.character1.body = 5
        self.level.add_creature(self.character1, (5, 5))

        self.character2.speed = 1
        self.character2.tick = 1
        self.character2.hit_points = 10
        self.character2.attack = 3
        self.character2.body = 5
        self.level.add_creature(self.character2, (6, 5))

    def test_get_unarmed_action(self):
        """
        Test that unarmed combat action can be generated
        """
        rng = StubRandomNumberGenerator()
        rng.inject(12, [12, 12, 12, 12, 12, 12, 12])

        action = self.action_factory.get_action(AttackParameters(
                                                      self.character1,
                                                      3,
                                                      'unarmed',
                                                      rng))

        assert isinstance(action,  AttackAction)
        assert action.attack_type == 'unarmed'

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

        assert self.character2.hit_points < 10

    def test_events_in_unarmed_combat(self):
        """
        Test that attacking raises events
        """
        character1 = Character(self.model,
                               self.action_factory,
                               self.rng)
        character1.attack = 12
        character1.speed = 1
        character1.tick = 0
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
        assert self.character2.hit_points == 10

        self.character1.execute_action(AttackParameters(
                                                self.character1,
                                                3,
                                                'melee',
                                                rng))

        assert self.character2.hit_points == 8
