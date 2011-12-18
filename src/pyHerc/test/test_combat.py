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

'''
Module for testing combat related rules
'''

import pyHerc
from pyHerc.data.dungeon import Level
from pyHerc.data.dungeon import Dungeon
from pyHerc.data.dungeon import Portal
from pyHerc.data.model import Model
from pyHerc.data.model import Character
from pyHerc.generators.dungeon import TestLevelGenerator
from pyHerc.rules.tables import Tables
from pyHerc.test import IntegrationTest
from pyHerc.test import StubRandomNumberGenerator

from pyHerc.rules.public import AttackParameters
from pyHerc.rules.public import ActionFactory
from pyHerc.rules.attack.action import AttackAction

class TestMeleeCombat(IntegrationTest):
    '''
    Class for testing melee combat related rules
    '''

    def setUp2(self):
        self.character1 = Character(self.action_factory)
        self.character2 = Character(self.action_factory)
        levelGenerator = TestLevelGenerator(self.action_factory)

        self.model.dungeon = Dungeon()
        self.level = levelGenerator.generate_level(None, self.model, monster_list = [])

        self.model.dungeon.levels = self.level

        self.character1.location = (5, 5)
        self.character1.level = self.model.dungeon.levels
        self.character1.speed = 1
        self.character1.tick = 1
        self.character1.hit_points = 10

        self.character2.location = (6, 5)
        self.character2.level = self.model.dungeon.levels
        self.character2.speed = 1
        self.character2.tick = 1
        self.character2.hit_points = 10

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
