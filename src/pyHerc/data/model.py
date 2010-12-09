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

class Model:
    """
    Represents playing world
    """

    def __init__(self):
        self.logger = logging.getLogger('pyHerc.data.model.Model')
        self.dungeon = None
        self.player = None
        self.config = None
        self.tables = None
        self.endCondition = 0

        self.logger.info('loading config')
        self.loadConfig()

    def loadConfig(self):
        """
        Loads config
        """
        self.config = {}
        self.config['level'] = {}
        self.config['level']['size']  = (80,  40)

    def raiseEvent(self, event):
        """
        Relays event to creatures
        Params:
            event : event to relay
        """
        self.logger.debug('raising event:' + event.__str__())
        #TODO: filter events
        for creature in event['level'].creatures:
            creature.receiveEvent(event)

        if self.player != None:
            self.player.receiveEvent(event)

class Character:
    """
    Represents a character in playing world
    """

    def __init__(self):
        # attributes
        self.str = None
        self.dex = None
        self.con = None
        self.int = None
        self.wis = None
        self.cha = None
        self.name = 'prototype'
        self.race = None
        self.kit = None
        self.hp = None
        self.speed = None
        self.inventory = []
        self.weapons = []
        #location
        self.level = None
        self.location = ()
        #icon
        self.icon = None
        #internal
        self.tick = 0
        self.shortTermMemory = []

    def __str__(self):
        return self.name

    def receiveEvent(self, event):
        """
        Receives an event from world and enters it into short term memory
        """
        self.shortTermMemory.append(event)

class Item:
    """
    Represents item
    """

    def __init__(self):
        #attributes
        self.name = 'prototype'
        self.questItem = 0
        #location
        self.location = ()
        #icon
        self.icon = None

    def __str__(self):
        return self.name
