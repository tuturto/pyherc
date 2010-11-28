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

import types
import os, sys
import logging
import random
import pyHerc.ai.simple
import pyHerc.data.model
import pyHerc.rules.tables
from pyHerc.data import tiles

class CreatureGenerator:
    """
    Class used to generate creatures
    """

    def __init__(self):
        self.logger = logging.getLogger('pyHerc.generators.creature.CreatureGenerator')
        pyHerc.rules.tables.loadTables()

    def generateCreature(self, parameters):
        """
        Generates a creature
        """
        self.logger.debug('generating a creature')
        self.logger.debug(parameters)
        newCreature = None
        if not parameters == None:
            if 'name' in parameters.keys():
                table = pyHerc.rules.tables.creatures[parameters['name']]
                newCreature = self.__generateCreatureFromTable(table)
        else:
            #generate completely random creature
            pass

        if newCreature == None:
            self.logger.warn('no creature generated')
        else:
            self.logger.debug('new creature generated: ' + newCreature.__str__())

        return newCreature

    def __generateCreatureFromTable(self, table):
        """
        Take table entry and generate corresponding creature
        """
        assert(table != None)

        newCreature = pyHerc.data.model.Character()
        newCreature.name = table['name']
        newCreature.str = table['str']
        newCreature.dex = table['dex']
        newCreature.con = table['con']
        newCreature.int = table['int']
        newCreature.wis = table['wis']
        newCreature.cha = table['cha']
        newCreature.hp = table['hp']
        newCreature.speed = table['speed']
        newCreature.size = table['size']
        newCreature.attack = table['attack']
        #TODO: AI from tables
        newCreature.act = types.MethodType(pyHerc.ai.simple.flockingHerbivore, newCreature, pyHerc.data.model.Character)


        if hasattr(table['icon'], 'append'):
            #select from list
            newCreature.icon = random.choice(table['icon'])
        else:
            newCreature.icon = table['icon']


        return newCreature
