#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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

from pyherc.data import Dungeon
from pyherc.aspects import logged

class DungeonGenerator(object):
    """
    This class is used to generate dungeon
    """
    @logged
    def __init__(self, creature_generator, item_generator,
                 level_generator):
        """
        Default constructor

        :param creature_generator: generator for creatures
        :param item_generator: generator for items
        :param level_generator: level generator for the first level
        """
        self.creature_generator = creature_generator
        self.item_generator = item_generator
        self.level_generator = level_generator

    @logged
    def generate_dungeon(self, model):
        """
        Generates start of the dungeon
        """
        model.dungeon = Dungeon()

        level = self.level_generator.generate_level(None)

        model.dungeon.levels = level

        portals = [x for x in level.portals
                   if x.exits_dungeon]
        exit = portals[0]

        level.add_creature(model.player, exit.location)
