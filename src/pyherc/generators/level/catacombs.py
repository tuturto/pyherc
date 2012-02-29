#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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
Classes for generating catacomb levels
"""

import logging
import random
import pyherc.generators.item
import pyherc.generators.creature
import pyherc.generators.utils
from pyherc.data.dungeon import Level
from pyherc.data.dungeon import Portal
from pyherc.data import tiles

class CatacombsLevelGenerator:
    """
    Generator for creating catacombs
    """

    def __init__(self, creature_generator, item_generator):
        """
        Default constructor

        Args:
            action_factory: Initialised action factory
            tables: Tables used in
        """
        self.logger = logging.getLogger('pyherc.generators.level.catacombs.CatacombsLevelGenerator') #pylint: disable=C0301
        self.item_generator = item_generator
        self.creature_generator = creature_generator

    def __getstate__(self):
        """
        Override __getstate__ in order to get pickling work
        """
        d = dict(self.__dict__)
        del d['logger']
        return d

    def __setstate__(self, d):
        """
        Override __setstate__ in order to get pickling work
        """
        self.__dict__.update(d)
        self.logger = logging.getLogger('pyherc.generators.level.catacombs.CatacombsLevelGenerator') #pylint: disable=C0301

    def generate_level(self, portal, model, new_portals = 0, level=1,
                                                room_min_size = (2, 2)):
        """
        Generate level that starts from given stairs

        Args:
            portal: link new level to this portal
            model: model being used
            new_portals: amount of portals to generate, default 0
            level: changes behaviour of the generator
            room_min_size: minimum size for rooms
        """
        self.logger.debug('generating level: {0}'.format(level))
        level_size = model.config['level']['size']
        BSPStack = []
        BSP = pyherc.generators.utils.BSPSection((0, 0),
                                                 (level_size[0] - 2,
                                                 level_size[1] - 2), None)
        BSPStack.append(BSP)
        room_stack = []

        temp_level = Level(level_size, tiles.FLOOR_ROCK, tiles.WALL_GROUND)

        while len(BSPStack) > 0:
            tempBSP = BSPStack.pop()
            tempBSP.split(min_size = (room_min_size[0] + 4,
                                      room_min_size[1] + 4))
            if tempBSP.node1 != None:
                BSPStack.append(tempBSP.node1)
            if tempBSP.node2 != None:
                BSPStack.append(tempBSP.node2)
            if tempBSP.node1 == None and tempBSP.node2 == None:
                #leaf
                room_stack.append(tempBSP)

        for room in room_stack:
            corner1 = (room.corner1[0] + random.randint(1, 4),
                       room.corner1[1] + random.randint(1, 4))
            corner2 = (room.corner2[0] - random.randint(1, 4),
                       room.corner2[1] - random.randint(1, 4))

            for y in range(corner1[1], corner2[1] + 1):
                for x in range(corner1[0], corner2[0] + 1):
                    temp_level.walls[x][y] = tiles.WALL_EMPTY

        area_queue = BSP.getAreaQueue()
        area_queue.reverse()

        while len(area_queue) > 1:
            area1 = area_queue.pop()
            area2 = area_queue.pop()
            center1 = area1.getCenter()
            center2 = area2.getCenter()
            #connect these two areas
            if area1.direction == 1:
                #areas on top of each other
                if center1[1] < center2[1]:
                    for y in range(center1[1], center2[1] + 1):
                        temp_level.walls[center1[0]][y] = tiles.WALL_EMPTY
                else:
                    for y in range(center2[1], center1[1] + 1):
                        temp_level.walls[center1[0]][y] = tiles.WALL_EMPTY
            else:
                #areas next to each other
                if center1[0] < center2[0]:
                    for x in range(center1[0], center2[0] + 1):
                        temp_level.walls[x][center1[1]] = tiles.WALL_EMPTY
                else:
                    for x in range(center2[0], center1[0] + 1):
                        temp_level.walls[x][center1[1]] = tiles.WALL_EMPTY

        #decorate dungeon a bit
        temp_walls = []
        for x in range(0, level_size[0] + 1):
            for y in range(0, level_size[1] + 1):
                if temp_level.walls[x][y] != tiles.WALL_EMPTY:
                    if y > 1:
                        temp_walls.append(temp_level.walls[x][y-1])
                        if x > 1:
                            temp_walls.append(temp_level.walls[x-1][y-1])
                        if x < level_size[0]:
                            temp_walls.append(temp_level.walls[x+1][y-1])
                    if y < level_size[1]:
                        temp_walls.append(temp_level.walls[x][y+1])
                        if x > 1:
                            temp_walls.append(temp_level.walls[x-1][y+1])
                        if x < level_size[0]:
                            temp_walls.append(temp_level.walls[x+1][y+1])
                    if x > 1:
                        temp_walls.append(temp_level.walls[x-1][y])
                    if x < level_size[0]:
                        temp_walls.append(temp_level.walls[x+1][y])
                    if tiles.WALL_EMPTY in temp_walls:
                        random_tile = random.randint(1, 100)
                        if random_tile == 98:
                            temp_level.walls[x][y] = tiles.WALL_ROCK_DECO_1
                        elif random_tile == 99:
                            temp_level.walls[x][y] = tiles.WALL_ROCK_DECO_2
                        else:
                            temp_level.walls[x][y] = tiles.WALL_ROCK
                temp_walls = []

        for i in range(0, 10):
            if level == 1:
                temp_creature = self.creature_generator.generate_creature(
                                            {'name':'rat'})
                temp_level.add_creature(temp_creature,
                                            temp_level.find_free_space())
            else:
                temp_creature = self.creature_generator.generate_creature(
                                                {'name':'fire beetle'})
                temp_level.add_creature(temp_creature,
                                        temp_level.find_free_space())

        #throw bunch of food items around
        for i in range(0, 10):
            temp_item = self.item_generator.generate_item({'type':'food'})
            temp_item.location = temp_level.find_free_space()
            temp_level.items.append(temp_item)

        for i in range(0, 3):
            temp_item = self.item_generator.generate_item({'type':'potion'})
            temp_item.location = temp_level.find_free_space()
            temp_level.items.append(temp_item)

        #throw bunch of weapons around
        for i in range(0, 10):
            temp_item = self.item_generator.generate_item({'type':'weapon'})
            temp_item.location = temp_level.find_free_space()
            temp_level.items.append(temp_item)

        if portal != None:
            new_portal = Portal()
            new_portal.model = model
            temp_level.add_portal(new_portal,
                                  temp_level.find_free_space(), portal)

        if new_portals > 0:
            for i in range(0, new_portals):
                new_portal = Portal()
                new_portal.model = model
                new_portal.icon = tiles.PORTAL_STAIRS_DOWN
                temp_level.add_portal(new_portal, temp_level.find_free_space())

        # generate next level
        for portal in temp_level.portals:
            if portal.get_other_end() == None:
                if level < 5:
                    new_level = self.generate_level(portal, model, 1,
                                                   level = level + 1)
                else:
                    pass

        self.logger.debug(temp_level.dump_string())
        return temp_level
