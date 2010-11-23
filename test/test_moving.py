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

import pyHerc.rules.moving

class test_moving:

    def setup(self):
        self.model = Model()
        self.character = Character()
        generator = TestLevelGenerator()

        self.model.dungeon = Dungeon()
        self.level1 = generator.generateLevel(None, self.model)
        self.level2 = generator.generateLevel(None, self.model)
        self.portal1 = Portal()
        self.portal1.icon = pyHerc.data.tiles.portal_stairs
        self.portal2 = Portal()

        self.level1.addPortal(self.portal1, (5, 5))
        self.level2.addPortal(self.portal2, (10, 10), self.portal1)

        self.model.dungeon.levels = self.level1

        self.character.location = (5, 5)
        self.character.level = self.model.dungeon.levels
        self.character.speed = 1
        self.character.tick = 1

    def test_simpleMoving(self):
        """
        Test that taking single step is possible
        """
        assert(self.character.location == (5, 5))
        pyHerc.rules.moving.move(self.model, self.character, 3)
        assert(self.character.location == (6, 5))

    def test_walkingToWalls(self):
        """
        Test that it is not possible to walk through walls
        """
        self.character.location = (1, 1)

        assert(self.character.location == (1, 1))
        pyHerc.rules.moving.move(self.model, self.character, 1)
        assert(self.character.location == (1, 1))

    def test_enteringPortal(self):
        """
        Test that character can change level via portal
        """
        assert(self.character.location == (5, 5))
        assert(self.character.level == self.level1)

        pyHerc.rules.moving.move(self.model, self.character, 9)

        assert(self.character.location == (10, 10))
        assert(self.character.level == self.level2)

    def test_enteringNonExistentPortal(self):
        """
        Test that character can change level via portal
        """
        self.character.location = (6, 3)
        assert(self.character.level == self.level1)

        pyHerc.rules.moving.move(self.model, self.character, 9)

        assert(self.character.location == (6, 3))
        assert(self.character.level == self.level1)
