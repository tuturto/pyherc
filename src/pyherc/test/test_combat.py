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

'''
Module for testing combat related rules
'''

import pyherc
from pyherc.data.dungeon import Dungeon
from pyherc.data.model import Character
from pyherc.generators.level.testlevel import TestLevelGenerator
from pyherc.test import IntegrationTest
from pyherc.test import StubRandomNumberGenerator

from pyherc.rules.public import AttackParameters
from pyherc.rules.attack.action import AttackAction

class TestMeleeCombat(IntegrationTest):
    '''
    Class for testing melee combat related rules
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        IntegrationTest.__init__(self)
        self.model = None
        self.level = None
        self.character1 = None
        self.character2 = None

    def setup2(self):
        self.character1 = Character(self.action_factory)
        self.character2 = Character(self.action_factory)
        level_generator = TestLevelGenerator(self.action_factory)

        self.model.dungeon = Dungeon()
        self.level = level_generator.generate_level(None,
                                                   self.model,
                                                   monster_list = [])

        self.model.dungeon.levels = self.level

        self.character1.location = (5, 5)
        self.character1.level = self.model.dungeon.levels
        self.character1.speed = 1
        self.character1.tick = 1
        self.character1.hit_points = 10
        self.character1.attack = 3
        self.character1.set_body(5)

        self.character2.location = (6, 5)
        self.character2.level = self.model.dungeon.levels
        self.character2.speed = 1
        self.character2.tick = 1
        self.character2.hit_points = 10
        self.character2.attack = 3
        self.character2.set_body(5)

    def test_get_unarmed_action(self):
        '''
        Test that unarmed combat action can be generated
        '''
        rng = StubRandomNumberGenerator()
        rng.inject(12, [12, 12, 12, 12, 12, 12, 12])

        action = self.action_factory.get_action(AttackParameters(
                                                      self.character1,
                                                      self.character2,
                                                      'unarmed',
                                                      rng))

        assert isinstance(action,  AttackAction)
        assert action.attack_type == 'unarmed'

    def test_unarmed_attack(self):
        '''
        Test that unarmed attack will harm opponent
        '''
        rng = StubRandomNumberGenerator()
        rng.inject(12, [2, 2, 2, 2, 2, 2, 2])

        self.character1.execute_action(AttackParameters(
                                                self.character1,
                                                self.character2,
                                                'unarmed',
                                                rng))

        assert self.character2.hit_points < 10

    def test_attack_with_weapon(self):
        '''
        Test that attack with a weapon will reduce targets hit points
        '''
        rng = StubRandomNumberGenerator()
        rng.inject(12, [2, 2, 2, 2, 2, 2, 2])

        dagger = self.item_generator.generate_item(self.tables,
                                                    {'name': 'dagger'})

        pyherc.rules.items.wield(self.model, self.character1, dagger)
        assert self.character2.hit_points == 10

        self.character1.execute_action(AttackParameters(
                                                self.character1,
                                                self.character2,
                                                'melee',
                                                rng))

        assert self.character2.hit_points == 8
