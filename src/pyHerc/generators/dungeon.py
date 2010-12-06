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
import pyHerc.generators.creature
import utils
from pyHerc.data.dungeon import Level
from pyHerc.data.dungeon import Dungeon
from pyHerc.data.dungeon import Portal
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
        generator = CatacombsLevelGenerator()
        level = generator.generateLevel(None, model, 2)

        model.dungeon.levels = level

        for portal in level.portals:
            newLevel = generator.generateLevel(portal, model, 0, level = 2)

        itemGenerator = pyHerc.generators.item.ItemGenerator()
        skull = itemGenerator.generateSpecialItem(model.tables, {'name':'crystal skull'})

        #TODO: write utility function for placing objects
        levelSize = model.config['level']['size']
        location = (random.randint(2, levelSize[0]-1), random.randint(2, levelSize[1]-1))
        while level.walls[location[0]][location[1]] != tiles.wall_empty:
            location = (random.randint(2, levelSize[0]-1), random.randint(2, levelSize[1]-1))
        level.addItem(skull, location)

        escapePortal = Portal()
        escapePortal.icon = pyHerc.data.tiles.portal_stairs_up
        escapePortal.otherEnd = None

        location = (random.randint(2, levelSize[0]-1), random.randint(2, levelSize[1]-1))
        while level.walls[location[0]][location[1]] != tiles.wall_empty:
            location = (random.randint(2, levelSize[0]-1), random.randint(2, levelSize[1]-1))
        level.addPortal(escapePortal, location)

        model.player.location = location

class CatacombsLevelGenerator:
    """
    Generator for creating catacombs
    """

    def __init__(self):
        self.logger = logging.getLogger('pyHerc.generators.dungeon.CatacombsLevelGenerator')
        self.itemGenerator = pyHerc.generators.item.ItemGenerator()
        self.creatureGenerator = pyHerc.generators.creature.CreatureGenerator()

    def generateLevel(self, portal, model, newPortals = 0, level=1, roomMinSize = (6, 6)):
        """
        Generate level that starts from given stairs
        Parameters:
            stairs : link new level to this portal
            model : model being used
            newPortals : amount of portals to generate, default 0
            level : changes behaviour of the generator
            roomMinSize : minimum size for rooms
        """
        self.logger.debug('generating level')
        levelSize = model.config['level']['size']
        self.logger.debug('dividing level in sections')
        BSPStack = []
        BSP = utils.BSPSection((0, 0), (levelSize[0] - 2, levelSize[1] - 2), None)
        BSPStack.append(BSP)
        roomStack = []

        tempLevel = Level(levelSize, tiles.floor_rock, tiles.wall_ground)
        #TODO: split into smaller chuncks
        while len(BSPStack) > 0:
            tempBSP = BSPStack.pop()
            tempBSP.split(minSize = (roomMinSize[0] + 4, roomMinSize[1] + 4))
            if tempBSP.node1 != None:
                BSPStack.append(tempBSP.node1)
            if tempBSP.node2 != None:
                BSPStack.append(tempBSP.node2)
            if tempBSP.node1 == None and tempBSP.node2 == None:
                #leaf
                roomStack.append(tempBSP)

        self.logger.debug('carving rooms')
        for room in roomStack:
            corner1 = (room.corner1[0] + random.randint(1, 4), room.corner1[1] + random.randint(1, 4))
            corner2 = (room.corner2[0] - random.randint(1, 4), room.corner2[1] - random.randint(1, 4))
            self.logger.debug('carving room ' + corner1.__str__() + ':' + corner2.__str__())
            for y in range(corner1[1], corner2[1] + 1):
                for x in range(corner1[0], corner2[0] + 1):
                    tempLevel.walls[x][y] = tiles.wall_empty

        self.logger.debug('carving tunnels')

        areaQueue = BSP.getAreaQueue()
        areaQueue.reverse()

        while len(areaQueue) > 1:
            area1 = areaQueue.pop()
            area2 = areaQueue.pop()
            center1 = area1.getCenter()
            center2 = area2.getCenter()
            self.logger.debug('carving tunnel between areas ' + area1.__str__() + ' and ' +
                                        area2.__str__())
            self.logger.debug('using center points ' + center1.__str__() + ' and ' +
                                        center2.__str__())
            #connect these two areas
            if area1.direction == 1:
                #areas on top of each other
                if center1[1] < center2[1]:
                    self.logger.debug('tunneling top down ' + center1[0].__str__() + ':' +
                                                range(center1[1], center2[1]).__str__())
                    for y in range(center1[1], center2[1] + 1):
                        tempLevel.walls[center1[0]][y] = tiles.wall_empty
                else:
                    self.logger.debug('tunneling top down ' + center1[0].__str__() + ':' +
                                                range(center2[1], center1[1]).__str__())
                    for y in range(center2[1], center1[1] + 1):
                        tempLevel.walls[center1[0]][y] = tiles.wall_empty
            else:
                #areas next to each other
                if center1[0] < center2[0]:
                    self.logger.debug('tunneling sideways ' + range(center1[0], center2[0]).__str__() +
                                                ':' + center1[1].__str__())
                    for x in range(center1[0], center2[0] + 1):
                        tempLevel.walls[x][center1[1]] = tiles.wall_empty
                else:
                    self.logger.debug('tunneling sideways ' + range(center2[0], center1[0]).__str__() +
                                                ':' + center1[1].__str__())
                    for x in range(center2[0], center1[0] + 1):
                        tempLevel.walls[x][center1[1]] = tiles.wall_empty

        #decorate dungeon a bit
        tempWalls = []
        for x in range(0, levelSize[0] + 1):
            for y in range(0, levelSize[1] + 1):
                if tempLevel.walls[x][y] != tiles.wall_empty:
                    if y > 1:
                        tempWalls.append(tempLevel.walls[x][y-1])
                        if x > 1:
                            tempWalls.append(tempLevel.walls[x-1][y-1])
                        if x < levelSize[0]:
                            tempWalls.append(tempLevel.walls[x+1][y-1])
                    if y < levelSize[1]:
                        tempWalls.append(tempLevel.walls[x][y+1])
                        if x > 1:
                            tempWalls.append(tempLevel.walls[x-1][y+1])
                        if x < levelSize[0]:
                            tempWalls.append(tempLevel.walls[x+1][y+1])
                    if x > 1:
                        tempWalls.append(tempLevel.walls[x-1][y])
                    if x < levelSize[0]:
                        tempWalls.append(tempLevel.walls[x+1][y])
                    if tiles.wall_empty in tempWalls:
                        randTile = random.randint(1, 100)
                        if randTile == 98:
                            tempLevel.walls[x][y] = tiles.wall_rock_deco_1
                        elif randTile == 99:
                            tempLevel.walls[x][y] = tiles.wall_rock_deco_2
                        else:
                            tempLevel.walls[x][y] = tiles.wall_rock
                tempWalls = []

        #enter few rats
        for i in range(0, 10):
            #TODO: better placement algorithm
            tempCreature = self.creatureGenerator.generateCreature(model.tables, {'name':'rat'})
            location = (random.randint(2, levelSize[0]-1), random.randint(2, levelSize[1]-1))
            while tempLevel.walls[location[0]][location[1]] != tiles.wall_empty:
                location = (random.randint(2, levelSize[0]-1), random.randint(2, levelSize[1]-1))
            tempLevel.addCreature(tempCreature, location)

        #throw bunch of food items around
        for i in range(0, 10):
            #TODO: better placement algorithm
            tempItem = self.itemGenerator.generateItem(model.tables, {'type':'food'})
            location = (random.randint(2, levelSize[0]-1), random.randint(2, levelSize[1]-1))
            while tempLevel.walls[location[0]][location[1]] != tiles.wall_empty:
                location = (random.randint(2, levelSize[0]-1), random.randint(2, levelSize[1]-1))
            tempItem.location = location
            tempLevel.items.append(tempItem)

        #throw bunch of weapons around
        for i in range(0, 10):
            #TODO: better placement algorithm
            tempItem = self.itemGenerator.generateItem(model.tables, {'type':'weapon'})
            location = (random.randint(2, levelSize[0]-1), random.randint(2, levelSize[1]-1))
            while tempLevel.walls[location[0]][location[1]] != tiles.wall_empty:
                location = (random.randint(2, levelSize[0]-1), random.randint(2, levelSize[1]-1))
            tempItem.location = location
            tempLevel.items.append(tempItem)

        if portal != None:
            newPortal = Portal()
            while tempLevel.walls[location[0]][location[1]] != tiles.wall_empty:
                location = (random.randint(2, levelSize[0]-1), random.randint(2, levelSize[1]-1))
            tempLevel.addPortal(newPortal, location, portal)

        if newPortals > 0:
            for i in range(0, newPortals):
                newPortal = Portal()
                newPortal.icon = tiles.portal_stairs_down
                while tempLevel.walls[location[0]][location[1]] != tiles.wall_empty:
                    location = (random.randint(2, levelSize[0]-1), random.randint(2, levelSize[1]-1))
                tempLevel.addPortal(newPortal, location)

        return tempLevel

class TestLevelGenerator:
    """
    Generates a simple test level
    """
    def __init__(self):
        self.logger = logging.getLogger('pyHerc.generators.dungeon.TestLevelGenerator')
        self.itemGenerator = pyHerc.generators.item.ItemGenerator()
        self.creatureGenerator = pyHerc.generators.creature.CreatureGenerator()

    def generateLevel(self, portal, model, newPortals = 0, monsterList = None):
        """
        Generate level that starts from given stairs
        Parameters:
            stairs : link new level to this portal
            model : model being used
            newPortals : amount of portals to generate, default 0
            monsterList : list of monsters to use
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

        #throw bunch of food around
        for i in range(0, 10):
            #TODO: better placement algorithm
            tempItem = self.itemGenerator.generateItem(model.tables, {'type':'food'})
            tempItem.location = (random.randint(2, 20), random.randint(2, 20))
            tempLevel.items.append(tempItem)

        if monsterList == None:
            #enter few rats
            for i in range(0, 5):
                #TODO: better placement algorithm
                tempCreature = self.creatureGenerator.generateCreature(model.tables.creatures, {'name':'rat'})
                tempLevel.addCreature(tempCreature, (random.randint(2, 20), random.randint(2, 20)))
        else:
            #TODO: spread given monsters around
            pass

        #set portals
        if portal != None:
            newPortal = pyHerc.data.dungeon.Portal()
            tempLevel.addPortal(newPortal, (random.randint(2, 20), random.randint(2, 20)), portal)

        if newPortals > 0:
            for i in range(0, newPortals):
                newPortal = pyHerc.data.dungeon.Portal()
                newPortal.icon = pyHerc.data.tiles.portal_stairs
                tempLevel.addPortal(newPortal, (random.randint(2, 20), random.randint(2, 20)))

        return tempLevel
