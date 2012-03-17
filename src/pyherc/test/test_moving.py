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
Module for testing moving
"""
#pylint: disable=W0614
from mockito import mock, verify, when, any
from hamcrest import * #pylint: disable=W0401

import pyherc
from pyherc.data.dungeon import Dungeon
from pyherc.data.dungeon import Portal
from pyherc.data.model import Character
from pyherc.generators.level.testlevel import TestLevelGenerator
from pyherc.test import IntegrationTest

import pyherc.rules.moving

class TestMoving(IntegrationTest):
    """
    Tests for moving
    """

    def __init__(self):
        """
        Default constructor
        """
        IntegrationTest.__init__(self)

    def setup2(self):
        """
        Secondary setup
        """
        self.character = Character(self.action_factory)
        levelGenerator = TestLevelGenerator(self.action_factory,
                                            self.creatureGenerator,
                                            self.item_generator)

        self.model.dungeon = Dungeon()
        self.level1 = levelGenerator.generate_level(None, self.model, monster_list = [])
        self.level2 = levelGenerator.generate_level(None, self.model, monster_list = [])
        self.portal1 = Portal((None, None), None)
        self.portal1.model = self.model
        self.portal1.icon = pyherc.data.tiles.PORTAL_STAIRS_DOWN
        self.portal2 = Portal((None, None), None)
        self.portal2 = Portal((None, None), None)
        self.portal2.model = self.model

        self.level1.add_portal(self.portal1, (5, 5))
        self.level2.add_portal(self.portal2, (10, 10), self.portal1)

        self.model.dungeon.levels = self.level1

        self.level1.add_creature(self.character, (5, 5))
        self.character.speed = 1
        self.character.tick = 1

    def test_simple_move(self):
        """
        Test that taking single step is possible
        """
        assert(self.character.location == (5, 5))

        self.character.move(3)

        assert(self.character.location == (6, 5))

    def test_walking_to_walls(self):
        """
        Test that it is not possible to walk through walls
        """
        self.character.location = (1, 1)

        self.character.move(1)

        assert(self.character.location == (1, 1))

    def test_entering_portal(self):
        """
        Test that character can change level via portal
        """
        assert(self.character.location == (5, 5))
        assert(self.character.level == self.level1)

        self.character.move(9)

        assert(self.character.location == (10, 10))
        assert(self.character.level == self.level2)

    def test_entering_portal_adds_character_to_creatures(self):
        """
        Test that entering portal will add character to the creatures list
        """
        assert self.character.level == self.level1
        assert self.character in self.level1.creatures

        self.character.move(9)

        assert self.character.level == self.level2
        assert self.character in self.level2.creatures

    def test_entering_portal_removes_character_from_old_level(self):
        """
        Test that entering portal will remove character from level
        """
        assert self.character.level == self.level1
        assert self.character in self.level1.creatures

        self.character.move(9)

        assert self.character not in self.level1.creatures

    def test_entering_non_existent_portal(self):
        """
        Test that character can not walk through floor
        """
        self.character.location = (6, 3)
        assert(self.character.level == self.level1)

        self.character.move(9)

        assert(self.character.location == (6, 3))
        assert(self.character.level == self.level1)

    def test_moving_uses_time(self):
        """
        Test that moving around uses time
        """
        tick = self.character.tick

        self.character.move(3)

        assert self.character.tick > tick
