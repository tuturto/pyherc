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
Module for dungeon generation
'''

import logging
import random
import pyherc.generators.item
import pyherc.generators.creature
import pyherc.generators.utils
from pyherc.generators.level.catacombs import CatacombsLevelGenerator
from pyherc.data.dungeon import Level
from pyherc.data.dungeon import Dungeon
from pyherc.data.dungeon import Portal
from pyherc.data import tiles

class DungeonGenerator:
    """
    This class is used to generate dungeon
    """

    def __init__(self, action_factory):
        self.logger = logging.getLogger('pyherc.generators.dungeon.DungeonGenerator')
        self.action_factory = action_factory

    def generate_dungeon(self, model):
        """
        Generates start of the dungeon
        """
        self.logger.info('generating the dungeon')
        model.dungeon = Dungeon()
        generator = CatacombsLevelGenerator(self.action_factory)
        level = generator.generate_level(None, model, 1)

        model.dungeon.levels = level

        escape_portal = Portal()
        escape_portal.icon = pyherc.data.tiles.PORTAL_STAIRS_UP
        escape_portal.set_other_end(None)
        #TODO: refactor for configuration
        escape_portal.model = model

        level_size = model.config['level']['size']
        location = (random.randint(2, level_size[0]-1),
                                        random.randint(2, level_size[1]-1))
        while level.walls[location[0]][location[1]] != tiles.WALL_EMPTY:
            location = (random.randint(2, level_size[0]-1),
                                        random.randint(2, level_size[1]-1))
        level.add_portal(escape_portal, location)

        model.player.location = location
