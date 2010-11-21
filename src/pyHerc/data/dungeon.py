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

import logging
import tiles

class Level:
    """
    Represents a level
    """

    def __init__(self):
        self.floor = None
        self.walls = None
        self.items = []
        self.portals = []
        self.creatures = []
        self.logger = logging.getLogger('pyHerc.data.dungeon.Level')

    def __init__(self, size, floorType, wallType):
        """
        Initialises a level of certain size and fill floor and walls with given types
        """
        self.logger = logging.getLogger('pyHerc.data.dungeon.Level')

        self.floor = []
        for y in range(0, size[0]):
            temp_row = []
            for y in range(0, size[1]):
                temp_row.append(floorType)
            self.floor.append(temp_row)

        self.walls = []
        for y in range(0, size[0]):
            temp_row = []
            for y in range(0, size[1]):
                temp_row.append(wallType)
            self.walls.append(temp_row)

        self.items = []
        self.portals = []
        self.creatures = []

    def addItem(self, item, location):
        """
        Add an item to this level
        Parameters:
            item : item to add
            location : location where to put the item
        """
        assert(not item == None)
        assert(not location == None)

        self.items.append(item)
        item.location = location

    def getItemsAt(self, location):
        """
        Get list of items at location
        Parameters:
            location : location to check
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
        Parameters:
            portal : portal to add
            location : location where to add portal
            otherEnd : optional other end of the portal
        """
        assert(portal != None)
        assert(location != None)

        portal.level = self
        portal.location = location
        self.portals.append(portal)

        if otherEnd != None:
            assert(otherEnd.icon != None or portal.icon != None)

            portal.otherEnd = otherEnd
            otherEnd.otherEnd = portal
            if portal.icon != None:
                otherEnd.icon = portal.icon
            else:
                portal.icon = otherEnd.icon

    def getPortalAt(self, location):
        """
        Check if there is a portal at given location
        Returns:
            Portal if found
            Otherwise None
        """
        for portal in self.portals:
            if portal.location == location:
                return portal

        return None

    def addCreature(self, creature, location = None):
        assert(creature != None)

        self.creatures.append(creature)
        creature.level = self
        if location != None:
            creature.location = location

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
        self.otherEnd = None
        self.questEnd = 0
        self.logger = logging.getLogger('pyHerc.data.dungeon.Portal')
