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
from data.dungeon import Level
from data.dungeon import Dungeon
from data import tiles

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
        model.dungeon.levels = generator.generateLevel(None, model)

class TestLevelGenerator:
    """
    Generates a simple test level
    """
    def __init__(self):
        self.logger = logging.getLogger('pyHerc.generators.dungeon.TestLevelGenerator')

    def generateLevel(self, stairs, model):
        """
        Generate level that starts from given stairs
        Will perform linking and required modifications to set up the model
        """
        self.logger.debug('creating a test level')
        tempLevel = Level(model.config['level']['size'], tiles.floor_rock, tiles.wall_empty)
