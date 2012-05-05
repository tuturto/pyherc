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

    def __init__(self, tables):
        """
        Default constructor

        Args:
            tables: Tables to use
        """
        self.logger = logging.getLogger('pyherc.generators.item.ItemGenerator')
        self.tables = tables

    def generate_item(self, parameters):
        """
        Generates an item
        """
        new_item = None
        if not parameters == None:
            if 'name' in parameters.keys():
                table = self.tables.items[parameters['name']]
                new_item = self.generate_item_from_table(table)
            elif 'type' in parameters.keys():
                rarity_range = self.tables.tag_score[parameters['type']]
                score = random.randint(1, rarity_range)
                for item in self.tables.items_by_tag[parameters['type']]:
                    if item[1] <= score and item[2] >= score:
                        choice = item[0]
                table = self.tables.items[choice]
                new_item = self.generate_item_from_table(table)
            else:
                #generate completely random item?
                pass
        else:
            #generate completely random item
            pass

        return new_item

    def generate_special_item(self, parameters):
        """
        Generate a special item

        Args:
            parameters: hash table containing parameters for generation
        """
        assert(parameters != None)
        assert('name' in parameters.keys())

        table = self.tables.items[parameters['name']]
        new_item = self.generate_item_from_table(table)

        return new_item

    def generate_item_from_table(self, table):
        """
        Take table entry and generate corresponding item
        """
        assert(table != None)

        new_item = Item()
        new_item.name = table['name']
        if hasattr(table['icon'], 'append'):
            #select from list
            new_item.icon = random.choice(table['icon'])
        else:
            new_item.icon = table['icon']

        if 'questItem' in table.keys():
            new_item.quest_item = table['questItem']

        new_item.cost = table['cost']
        new_item.weight = table['weight']
        new_item.rarity = table['rarity']

        #weapon related attributes
        if 'damage' in table.keys():
            new_item.weapon_data = WeaponData(
                                    damage = table['damage'],
                                    critical_range = table['critical range'],
                                    critical_damage = table['critical damage'],
                                    damage_type = table['damage type'],
                                    weapon_type = table['class'])

        new_item.tags = table['type']

        if 'charges' in table.keys():
            new_item.charges = table['charges']

        if 'effects' in table.keys():
            new_item.effects = {}
            keys = table['effects'].keys()

            for effect_type in keys:
                new_item.effects[effect_type] = []
                for effect in table['effects'][effect_type]:
                    #TODO: temporary hack
                    new_effect = ItemEffectData(trigger = effect_type,
                                       effect = effect['name'],
                                       parameters = effect['power'],
                                       charges = 1)

                new_item.effects[effect_type].append(new_effect)

        if 'appearance' in table.keys():
            new_item.appearance = table['appearance']

        return new_item
