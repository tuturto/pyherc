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

import random
import logging
import tiles

class Level:
    """
    Represents a level
    """
    def __init__(self, size = (0, 0), floorType = None, wallType = None):
        """
        Initialises a level of certain size and fill floor and walls with given types
        """
        self.logger = logging.getLogger('pyHerc.data.dungeon.Level')

        self.floor = []
        self.walls = []
        self.lit = []

        if size[0] != 0 and size[1] != 0:
            for y in range(0, size[0] + 1):
                temp_row = []
                for y in range(0, size[1] + 1):
                    temp_row.append(floorType)
                self.floor.append(temp_row)

            for y in range(0, size[0] + 1):
                temp_row = []
                for y in range(0, size[1] + 1):
                    temp_row.append(wallType)
                self.walls.append(temp_row)

        self.items = []
        self.portals = []
        self.creatures = []
        self.full_update_needed = True
        self.dirty_rectangles = []

    def get_tile(self, loc_x, loc_y):
        '''
        Get tile at given location
        @param loc_x: x-coordinate of the location
        @param loc_y: y-coordinate of the location
        '''
        if loc_x < 0 or loc_y < 0:
            return tiles.floor_empty

        if loc_x > len(self.floor) or loc_y > len(self.floor[0]):
            return tiles.floor_empty

        if self.walls[loc_x][loc_y] != tiles.wall_empty:
            return self.walls[loc_x][loc_y]
        else:
            return self.floor[loc_x][loc_y]

    def get_wall_tile(self, loc_x, loc_y):
        '''
        Get wall tile at given location
        @param loc_x: x-coordinate of the location
        @param loc_y: y-coordinate of the location
        '''
        if loc_x < 0 or loc_y < 0:
            return tiles.wall_ground

        if loc_x > len(self.floor) or loc_y > len(self.floor[0]):
            return tiles.wall_ground

        return self.walls[loc_x][loc_y]

    def addItem(self, item, location):
        """
        Add an item to this level
        @param item: item to add
        @param location: location where to put the item
        """
        assert(not item == None)
        assert(not location == None)

        self.logger.debug('adding an item: ' + item.__str__() +
                                ' to location: ' + location.__str__())
        self.items.append(item)
        item.location = location

    def getItemsAt(self, location):
        """
        Get list of items at location
        @param location: location to check
        """
        assert(location != None)
        items = []
        for item in self.items:
            if item.location == location:
                items.append(item)
        return items

    def addPortal(self, portal, location, otherEnd = None):
        """
        Adds precreated portal on level at given location
        If secondary portal is specified, link them together
        @param portal: portal to add
        @param location: location where to add portal
        @param otherEnd: optional other end of the portal
        """
        assert(portal != None)
        assert(location != None)

        self.logger.debug('adding a portal to location: ' + location.__str__())

        portal.level = self
        portal.location = location
        self.portals.append(portal)

        if otherEnd != None:
            assert(otherEnd.icon != None or portal.icon != None)

            portal.setOtherEnd (otherEnd)
            otherEnd.setOtherEnd(portal)
            if portal.icon != None:
                if otherEnd.icon == None:
                    if portal.icon == tiles.portal_stairs_down:
                        otherEnd.icon = tiles.portal_stairs_up
                    else:
                        otherEnd.icon = tiles.portal_stairs_down
            else:
                if otherEnd.icon == tiles.portal_stairs_down:
                    portal.icon = tiles.portal_stairs_up
                else:
                    portal.icon = tiles.portal_stairs_down

    def getPortalAt(self, location):
        """
        Check if there is a portal at given location
        @return: Portal if found, otherwise None
        """
        for portal in self.portals:
            if portal.location == location:
                return portal

        return None

    def addCreature(self, creature, location = None):
        """
        Add a creature to level
        @param creature: creature to add
        @param location: optional location for the creature
        """
        assert(creature != None)

        if location == None:
            self.logger.debug('adding ' + creature.__str__())
        else:
            self.logger.debug('adding ' + creature.__str__()
                              + ' to location ' + location.__str__())

        self.creatures.append(creature)
        creature.level = self
        if location != None:
            creature.location = location

    def removeCreature(self, creature):
        """
        Remove creature from level
        @param creature: creature to remove
        """
        assert(creature != None)
        assert(creature in self.creatures)
        self.logger.debug('removing a creature: ' + creature.__str__())

        self.creatures.remove(creature)
        creature.level = None
        creature.location = ()

    def getCreatureAt(self, location):
        """
        Get list of creatures at given location
        @param location: location to check
        @return: creature if found
        """
        assert(location != None)
        for creature in self.creatures:
            if creature.location == location:
                return creature

        return None

    def findFreeSpace(self):
        """
        Finds free space where stuff can be placed
        """
        x = len(self.floor)
        y = len(self.floor[0])
        location = (random.randint(2, x - 1), random.randint(2, y - 1))
        while self.walls[location[0]][location[1]] != tiles.wall_empty:
            location = (random.randint(2, x - 1), random.randint(2, y - 1))
        return location

    def get_square(self, x_coordinate, y_coordinate):
        '''
        Get square at given coordinates
        '''
        if walls[x_coordinate][y_coordinate] != wall_empty:
            return walls[x][y]
        else:
            return floor[x_coordinate][y_coordinate]

    def blocks_los(self, x_coordinate, y_coordinate):
        '''
        Checks if there's LOS-blocking wall at given coordinates
        '''

        if walls[x_coordinate][y_coordinate] != wall_empty:
            return False
        else:
            return True

class Dungeon:
    """
    Represents the dungeon
    """

    def __init__(self):
        self.levels = None
        self.logger = logging.getLogger('pyHerc.data.dungeon.Dungeon')

class Portal:
    """
    Portal linking two levels together
    """

    def __init__(self):
        self.level = None
        self.location = ()
        self.icon = None
        self.__otherEnd = None
        self.questEnd = 0
        self.levelGenerator = None
        self.logger = logging.getLogger('pyHerc.data.dungeon.Portal')

    def getOtherEnd(self):
        return self.__otherEnd

    def setOtherEnd(self, portal):
        self.__otherEnd = portal

    def generateLevel(self, model):
        '''
        Generates level if this is a proxy portal
        '''
        assert self.levelGenerator != None
        self.logger.debug('generating a new level')

        #TODO: support for level generation parameters
        newLevel = self.levelGenerator.generateLevel(self, model, monsterList = [])

