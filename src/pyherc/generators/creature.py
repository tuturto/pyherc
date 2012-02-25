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
Module for creature generation related classes

Classes:
    CreatureGenerator
"""

import logging
import random
import pyherc.ai.simple
import pyherc.data.model
import pyherc.rules.tables

class CreatureGenerator:
    """
    Class used to generate creatures
    """

    def __init__(self, action_factory):
        """
        Default constructor

        Args:
            action_factory: Initialised action factory
        """
        self.logger = logging.getLogger(
                            'pyherc.generators.creature.CreatureGenerator')
        self.action_factory = action_factory

    def generate_creature(self, tables, parameters):
        """
        Generates a creature

        Args:
            tables: tables used in generation
            parameters: hash table containing parameters
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

        new_creature = pyherc.data.model.Character(self.action_factory)
        new_creature.name = table['name']
        new_creature.set_body(table['body'])
        new_creature.set_finesse(table['finesse'])
        new_creature.set_mind(table['mind'])
        new_creature.set_hp(table['hp'])
        new_creature.speed = table['speed']
        new_creature.size = table['size']
        new_creature.attack = table['attack']
        #TODO: AI from tables
        new_creature.artificial_intelligence = pyherc.ai.simple.FlockingHerbivore(new_creature)

        if hasattr(table['icon'], 'append'):
            #select from list
            new_creature.icon = random.choice(table['icon'])
        else:
            new_creature.icon = table['icon']

        return new_creature
