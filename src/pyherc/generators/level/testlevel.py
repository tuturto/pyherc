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
Classes for generating test levels
These levels are not used in game, their function is to help in testing
'''

import logging
import random
import pyherc.generators.item
import pyherc.generators.creature
import pyherc.generators.utils
from pyherc.data.dungeon import Level
from pyherc.data.dungeon import Portal
from pyherc.data import tiles
from pyherc.generators import ItemGenerator
from pyherc.generators import CreatureGenerator

class TestLevelGenerator:
    """
    Generates a simple test level
    """
    def __init__(self, action_factory):
        self.logger = logging.getLogger('pyherc.generators.level.testlevel.TestLevelGenerator')
        self.item_generator = ItemGenerator()
        self.creature_generator = CreatureGenerator(action_factory)

    def __getstate__(self):
        '''
        Override __getstate__ in order to get pickling work
        '''
        d = dict(self.__dict__)
        del d['logger']
        return d

    def __setstate__(self, d):
        '''
        Override __setstate__ in order to get pickling work
        '''
        self.__dict__.update(d)
        self.logger = logging.getLogger('pyherc.generators.level.testlevel.CatacombsLevelGenerator')

    def generate_level(self, portal, model,
                       new_portals = 0, monster_list = None):
        """
        Generate level that starts from given stairs
        @param portal: link new level to this portal
        @param model: model being used
        @param new_portals: amount of portals to generate, default 0
        @param monster_list: list of monsters to use
        """
        self.logger.debug('creating a test level')
        level_size = model.config['level']['size']
        temp_level = Level(level_size, tiles.FLOOR_ROCK, tiles.WALL_EMPTY)
        #TODO: implement properly
        for x in range(0, level_size[0]):
            temp_level.walls[x][0] = tiles.WALL_ROCK
            temp_level.walls[x][level_size[1]-1] = tiles.WALL_ROCK

        for y in range(0, level_size[1]):
            temp_level.walls[0][y] = tiles.WALL_ROCK
            temp_level.walls[level_size[0] - 1][y] = tiles.WALL_ROCK

        #throw bunch of food around
        for i in range(0, 10):
            #TODO: better placement algorithm
            temp_item = self.item_generator.generateItem(model.tables,
                                                         {'type':'food'})
            temp_item.location = (random.randint(2, 20), random.randint(2, 20))
            temp_level.items.append(temp_item)

        if monster_list == None:
            #enter few rats
            for i in range(0, 5):
                #TODO: better placement algorithm
                temp_creature = self.creature_generator.generate_creature(
                                                    model.tables.creatures,
                                                    {'name':'rat'})
                temp_level.add_creature(temp_creature,
                                        (random.randint(2, 20),
                                        random.randint(2, 20)))
        else:
            #TODO: spread given monsters around
            pass

        #set portals
        if portal != None:
            new_portal = Portal()
            #TODO: refactor for configuration
            new_portal.model = model
            temp_level.add_portal(new_portal,
                                  (random.randint(2, 20),
                                  random.randint(2, 20)), portal)

        if new_portals > 0:
            for i in range(0, new_portals):
                new_portal = Portal()
                #TODO: refactor for configuration
                new_portal.model = model
                new_portal.icon = pyherc.data.tiles.PORTAL_STAIRS_DOWN
                temp_level.add_portal(new_portal,
                                      (random.randint(2, 20),
                                      random.randint(2, 20)))

        return temp_level
