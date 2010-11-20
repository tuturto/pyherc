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

import os, sys
import logging
import random
import pyHerc.generators.item
from pyHerc.data.dungeon import Level
from pyHerc.data.dungeon import Dungeon
from pyHerc.data import tiles

class DungeonGenerator:
    """
    This class is used to generate dungeon
    """

    def __init__(self):
        self.logger = logging.getLogger('pyHerc.generators.dungeon.DungeonGenerator')

    def generateDungeon(self, model):
        """
        Generates start of the dungeon
        """
        self.logger.info('generating the dungeon')
        model.dungeon = Dungeon()
        generator = TestLevelGenerator()
        level = generator.generateLevel(None, model, 2)

        self.logger.debug('generating ' + len(level.portals).__str__() + ' sub levels')
        for portal in level.portals:
            newLevel = generator.generateLevel(portal, model)

        model.dungeon.levels = level

class TestLevelGenerator:
    """
    Generates a simple test level
    """
    def __init__(self):
        self.logger = logging.getLogger('pyHerc.generators.dungeon.TestLevelGenerator')
        self.itemGenerator = pyHerc.generators.item.ItemGenerator()

    def generateLevel(self, portal, model, newPortals = 0):
        """
        Generate level that starts from given stairs
        Parameters:
            stairs : link new level to this portal
            model : model being used
            newPortals : amount of portals to generate, default 0
        """
        self.logger.debug('creating a test level')
        levelSize = model.config['level']['size']
        tempLevel = Level(levelSize, tiles.floor_rock, tiles.wall_empty)
        #TODO: implement properly
        for x in range(0, levelSize[0]):
            tempLevel.walls[x][0] = tiles.wall_rock
            tempLevel.walls[x][levelSize[1]-1] = tiles.wall_rock

        for y in range(0, levelSize[1]):
            tempLevel.walls[0][y] = tiles.wall_rock
            tempLevel.walls[levelSize[0] - 1][y] = tiles.wall_rock

        #throw bunch of apples around
        for i in range(0, 10):
            #TODO: better placement algorithm
            tempItem = self.itemGenerator.generateFood({'name':'apple'})
            tempItem.location = (random.randint(2, 20), random.randint(2, 20))
            tempLevel.items.append(tempItem)

        if portal != None:
            newPortal = pyHerc.data.dungeon.Portal()
            tempLevel.addPortal(newPortal, (random.randint(2, 20), random.randint(2, 20)), portal)

        if newPortals > 0:
            for i in range(0, newPortals):
                newPortal = pyHerc.data.dungeon.Portal()
                newPortal.icon = pyHerc.data.tiles.portal_stairs
                tempLevel.addPortal(newPortal, (random.randint(2, 20), random.randint(2, 20)))

        return tempLevel
