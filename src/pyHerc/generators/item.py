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
import pyHerc.data.model
import pyHerc.rules.tables
from pyHerc.data import tiles

class ItemGenerator:
    """
    Class used to generate items
    """

    def __init__(self):
        self.logger = logging.getLogger('pyHerc.generators.item.ItemGenerator')

    def generateItem(self, tables, parameters):
        """
        Generates an item
        """
        self.logger.debug('generating an item')
        self.logger.debug(parameters)
        assert(tables != None)
        newItem = None
        if not parameters == None:
            #TODO: generate named items too?
            if 'type' in parameters.keys():
                if parameters['type'] == 'special':
                    #generate special item
                    newItem = self.generateSpecialItem(tables, parameters)
                elif parameters['type'] == 'food':
                    #generate food
                    newItem = self.generateFood(tables, parameters)
            else:
                #generate completely random item?
                pass
        else:
            #generate completely random item
            pass

        if newItem == None:
            self.logger.warn('no item generated')
        else:
            self.logger.debug('new item generated: ' + newItem.__str__())

        return newItem

    def generateFood(self, tables, parameters):
        """
        Generate a food item
        Parameters:
            tables : tables used in generation
            parameters : hash table containing parameters for generation
        """
        self.logger.debug('generating a food item')
        assert(tables != None)

        if parameters == None:
            #TODO: generate random food
            pass
        elif not 'name' in parameters.keys():
            #TODO: generate random food
            pass
        else:
            #generate named food
            table = tables[parameters['name']]
            newItem = self.__generateItemFromTable(table)

        self.logger.debug('food item generation done')

        return newItem


    def generateSpecialItem(self, tables, parameters):
        """
        Generate a special item
        Parameters:
            tables : tables used in generation
            parameters : hash table containing parameters for generation
        """
        assert(tables != None)
        assert(parameters != None)
        assert('name' in parameters.keys())

        self.logger.debug('generating a special item')

        table = tables[parameters['name']]
        newItem = self.__generateItemFromTable(table)

        self.logger.debug('special item generation done')

        return newItem

    def __generateItemFromTable(self, table):
        """
        Take table entry and generate corresponding item
        """
        assert(table != None)

        newItem = pyHerc.data.model.Item()
        newItem.name = table['name']
        newItem.icon = table['icon']

        if 'questItem' in table.keys():
            newItem.questItem = table['questItem']

        return newItem
