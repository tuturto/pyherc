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

import pyherc
from pyherc.data.dungeon import Level
from pyherc.data.dungeon import Dungeon
from pyherc.data.dungeon import Portal
from pyherc.data.model import Model
from pyherc.data.model import Character
from pyherc.generators.level.testlevel import TestLevelGenerator
from pyherc.rules.tables import Tables
from pyherc.test import IntegrationTest
from pyherc.test import StubModel

from pyherc.rules.public import MoveParameters
from pyherc.rules.public import ActionFactory
from pyherc.rules.move.factories import MoveFactory
from pyherc.rules.move.factories import WalkFactory

import pyherc.rules.moving

class TestMoving(IntegrationTest):

    def setUp2(self):
        self.character = Character(self.action_factory)
        levelGenerator = TestLevelGenerator(self.action_factory)

        self.model.dungeon = Dungeon()
        self.level1 = levelGenerator.generate_level(None, self.model, monster_list = [])
        self.level2 = levelGenerator.generate_level(None, self.model, monster_list = [])
        self.portal1 = Portal()
        #TODO: refactor for configuration
        self.portal1.model = self.model
        self.portal1.icon = pyherc.data.tiles.PORTAL_STAIRS_DOWN
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
        proxy.level_generator = TestLevelGenerator(self.action_factory)
        #TODO: refactor for configuration
        proxy.model = self.model
        proxy.icon = pyherc.data.tiles.PORTAL_STAIRS_DOWN

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
