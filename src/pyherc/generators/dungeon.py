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
Module for dungeon generation
"""

import logging
import random
import pyherc.generators.item
import pyherc.generators.creature
import pyherc.generators.utils
from pyherc.data.dungeon import Dungeon
from pyherc.data.dungeon import Portal
from pyherc.data import tiles
from pyherc.aspects import Logged

class DungeonGenerator:
    """
    This class is used to generate dungeon
    """
    logged = Logged()

    @logged
    def __init__(self, creature_generator, item_generator,
                 level_generator):
        """
        Default constructor

        Args:
            creature_generator: generator for creatures
            item_generator: generator for items
            level_generator: level generator for the first level
        """
        self.logger = logging.getLogger('pyherc.generators.dungeon.DungeonGenerator')
        self.creature_generator = creature_generator
        self.item_generator = item_generator
        self.level_generator = level_generator

    @logged
    def generate_dungeon(self, model):
        """
        Generates start of the dungeon
        """
        self.logger.info('generating the dungeon')
        model.dungeon = Dungeon()

        level = self.level_generator.generate_level(None)

        model.dungeon.levels = level

        level_size = level.get_size()
        location = (random.randint(2, level_size[0]-1),
                                        random.randint(2, level_size[1]-1))
        while level.walls[location[0]][location[1]] != tiles.WALL_EMPTY:
            location = (random.randint(2, level_size[0]-1),
                                        random.randint(2, level_size[1]-1))

        level.add_creature(model.player, location)
