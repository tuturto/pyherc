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
from pyHerc.data.dungeon import Level
from pyHerc.data.dungeon import Dungeon
from pyHerc.data.dungeon import Portal
from pyHerc.data.model import Model
from pyHerc.data.model import Character
from pyHerc.generators.dungeon import TestLevelGenerator
from pyHerc.rules.tables import Tables
from pyHerc.test import IntegrationTest

from pyHerc.rules.public import MoveParameters
from pyHerc.rules.public import ActionFactory
from pyHerc.rules.move.factories import MoveFactory
from pyHerc.rules.move.factories import WalkFactory

import pyHerc.rules.moving

class TestMoving(IntegrationTest):

    def setUp2(self):
        self.character = Character()
        levelGenerator = TestLevelGenerator()

        move_factory = MoveFactory(WalkFactory())
        self.action_factory = ActionFactory(move_factory)

        self.model.dungeon = Dungeon()
        self.level1 = levelGenerator.generate_level(None, self.model, monster_list = [])
        self.level2 = levelGenerator.generate_level(None, self.model, monster_list = [])
        self.portal1 = Portal()
        #TODO: refactor for configuration
        self.portal1.model = self.model
        self.portal1.icon = pyHerc.data.tiles.PORTAL_STAIRS_DOWN
        self.portal2 = Portal()
        #TODO: refactor for configuration
        self.portal2.model = self.model

        self.level1.add_portal(self.portal1, (5, 5))
        self.level2.add_portal(self.portal2, (10, 10), self.portal1)

        self.model.dungeon.levels = self.level1

        self.character.location = (5, 5)
        self.character.level = self.model.dungeon.levels
        self.character.speed = 1
        self.character.tick = 1

    def test_simple_move(self):
        '''
        Test that taking single step is possible
        '''
        assert(self.character.location == (5, 5))
        action = self.action_factory.get_action(
                            MoveParameters(
                                           self.character, 3, 'walk'))
        action.execute()
        assert(self.character.location == (6, 5))

    def test_walking_to_walls(self):
        """
        Test that it is not possible to walk through walls
        """
        self.character.location = (1, 1)

        assert(self.character.location == (1, 1))
        action = self.action_factory.get_action(
                            MoveParameters(
                                           self.character, 1, 'walk'))
        action.execute()
        assert(self.character.location == (1, 1))

    def test_entering_portal(self):
        """
        Test that character can change level via portal
        """
        assert(self.character.location == (5, 5))
        assert(self.character.level == self.level1)

        action = self.action_factory.get_action(
                            MoveParameters(
                                           self.character, 9, 'walk'))
        action.execute()

        assert(self.character.location == (10, 10))
        assert(self.character.level == self.level2)

    def test_entering_non_existent_portal(self):
        """
        Test that character can not walk through floor
        """
        self.character.location = (6, 3)
        assert(self.character.level == self.level1)

        action = self.action_factory.get_action(
                            MoveParameters(
                                           self.character, 9, 'walk'))
        action.execute()

        assert(self.character.location == (6, 3))
        assert(self.character.level == self.level1)

    def test_enter_proxy_portal(self):
        """
        Test that entering proxy portal actually moves character to different location
        """
        self.character.location = (8, 8)
        proxy = Portal()
        proxy.level_generator = TestLevelGenerator()
        #TODO: refactor for configuration
        proxy.model = self.model
        proxy.icon = pyHerc.data.tiles.PORTAL_STAIRS_DOWN

        self.level1.add_portal(proxy, (8, 8))
        action = self.action_factory.get_action(
                            MoveParameters(
                                           self.character, 9, 'walk'))
        action.execute()

        assert(self.character.level != self.level1)

    def test_moving_uses_time(self):
        '''
        Test that moving around uses time
        '''
        tick = self.character.tick
        action = self.action_factory.get_action(
                            MoveParameters(
                                           self.character, 3, 'walk'))
        action.execute()
        assert self.character.tick > tick
