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

'''
Module for creature generation related classes

Classes:
    CreatureGenerator
'''

import types
import logging
import random
import pyHerc.ai.simple
import pyHerc.data.model
import pyHerc.rules.tables

class CreatureGenerator:
    """
    Class used to generate creatures
    """

    def __init__(self, action_factory):
        self.logger = logging.getLogger(
                            'pyHerc.generators.creature.CreatureGenerator')
        self.action_factory = action_factory

    def generate_creature(self, tables, parameters):
        """
        Generates a creature
        @param tables: tables used in generation
        @param parameters: hash table containing parameters
        """
        self.logger.debug('generating a creature')
        self.logger.debug(parameters)
        assert(tables != None)

        new_creature = None
        if not parameters == None:
            if 'name' in parameters.keys():
                table = tables.creatures[parameters['name']]
                new_creature = self.generate_creature_from_table(table)
        else:
            #generate completely random creature
            pass

        if new_creature == None:
            self.logger.warn('no creature generated')
        else:
            self.logger.debug('new creature generated: '
                              + new_creature.__str__())

        return new_creature

    def generate_creature_from_table(self, table):
        """
        Take table entry and generate corresponding creature
        """
        assert(table != None)

        newCreature = pyHerc.data.model.Character(self.action_factory)
        newCreature.name = table['name']
        newCreature.str = table['str']
        newCreature.dex = table['dex']
        newCreature.con = table['con']
        newCreature.int = table['int']
        newCreature.wis = table['wis']
        newCreature.cha = table['cha']
        newCreature.hit_points = table['hp']
        newCreature.speed = table['speed']
        newCreature.size = table['size']
        newCreature.attack = table['attack']
        #TODO: AI from tables
        newCreature.artificial_intelligence = pyHerc.ai.simple.FlockingHerbivore(newCreature)


        if hasattr(table['icon'], 'append'):
            #select from list
            newCreature.icon = random.choice(table['icon'])
        else:
            newCreature.icon = table['icon']


        return newCreature
