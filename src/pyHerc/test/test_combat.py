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

from pyHerc.test import IntegrationTest
from pyHerc.rules.public import ActionFactory
from pyHerc.rules.public import AttackParameters
from pyHerc.data.model import Character
from pyHerc.data.dungeon import Level
from pyHerc.data import tiles

class TestMeleeCombat(IntegrationTest):
    '''
    Class for testing melee combat related rules
    '''

    def test_basic_melee_attack(self):
        '''
        Test that basic melee attack can be done
        '''
        level = Level(size = (20, 20), floor_type = tiles.FLOOR_BRICK,
                            wall_type = tiles.WALL_ROCK)

        character1 = Character()
        character2 = Character()

        level.add_creature(character1, (10, 10))
        level.add_creature(character2, (10, 11))

        factory = ActionFactory()
        action = factory.get_action(
                            AttackParameters(character1, character2, 'melee'))

        action.execute()
