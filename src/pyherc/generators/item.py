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
Classes needed for item generation
"""

import logging
import random
from pyherc.data.item import Item
from pyherc.data.item import WeaponData
from pyherc.data.item import ItemEffectData

class ItemGenerator:
    """
    Class used to generate items
    """

    def __init__(self):
        """
        Default constructor
        """
        self.logger = logging.getLogger('pyherc.generators.item.ItemGenerator')

    def generateItem(self, tables, parameters):
        """
        Generates an item
        """
        self.logger.debug('generating an item')
        self.logger.debug(parameters)
        assert(tables != None)
        newItem = None
        if not parameters == None:
            if 'name' in parameters.keys():
                table = tables.items[parameters['name']]
                newItem = self.__generateItemFromTable(table)
            elif 'type' in parameters.keys():
                rarityRange = tables.tagScore[parameters['type']]
                score = random.randint(1, rarityRange)
                for item in tables.itemsByTag[parameters['type']]:
                    if item[1] <= score and item[2] >= score:
                        choice = item[0]
                table = tables.items[choice]
                newItem = self.__generateItemFromTable(table)
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

    def generateSpecialItem(self, tables, parameters):
        """
        Generate a special item
        @param tables: tables used in generation
        @param parameters: hash table containing parameters for generation
        """
        assert(tables != None)
        assert(parameters != None)
        assert('name' in parameters.keys())

        self.logger.debug('generating a special item')

        table = tables.items[parameters['name']]
        newItem = self.__generateItemFromTable(table)

        self.logger.debug('special item generation done')

        return newItem

    def __generateItemFromTable(self, table):
        """
        Take table entry and generate corresponding item
        """
        assert(table != None)

        newItem = Item()
        newItem.name = table['name']
        if hasattr(table['icon'], 'append'):
            #select from list
            newItem.icon = random.choice(table['icon'])
        else:
            newItem.icon = table['icon']

        if 'questItem' in table.keys():
            newItem.quest_item = table['questItem']

        newItem.cost = table['cost']
        newItem.weight = table['weight']
        newItem.rarity = table['rarity']

        #weapon related attributes
        if 'damage' in table.keys():
            newItem.weapon_data = WeaponData(
                                    damage = table['damage'],
                                    critical_range = table['critical range'],
                                    critical_damage = table['critical damage'],
                                    damage_type = table['damage type'],
                                    weapon_type = table['class'])

        newItem.tags = table['type']

        if 'charges' in table.keys():
            newItem.charges = table['charges']

        if 'effects' in table.keys():
            newItem.effects = {}
            keys = table['effects'].keys()

            for effectType in keys:
                newItem.effects[effectType] = []
                for effect in table['effects'][effectType]:
                    #TODO: add support for charges
                    newEffect = ItemEffectData(trigger = effectType,
                                       effect_type = effect['name'],
                                       power = effect['power'])

                newItem.effects[effectType].append(newEffect)

        if 'appearance' in table.keys():
            newItem.appearance = table['appearance']

        return newItem
