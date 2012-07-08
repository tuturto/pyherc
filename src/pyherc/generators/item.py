#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
from pyherc.data import Item, EffectsCollection
from pyherc.data.item import WeaponData
from pyherc.rules.effects import EffectHandle
from pyherc.aspects import Logged

class NewItemGenerator(object):
    """
    Class used to generate items
    """
    logged = Logged()

    @logged
    def __init__(self, config):
        """
        Default constructor

        :param config: configuration for items
        :type config: ItemConfiguration
        """
        super(NewItemGenerator, self).__init__()
        self.config = config

    @logged
    def generate_item(self, name):
        """
        Generate an item

        :param name: name of the item to generate
        :type name: string
        :return: Generated item
        :rtype: Item
        """
        item_specification = self.find_item_specification(name)

        item = self.create_item(item_specification)

        return item

    @logged
    def find_item_specification(self, name):
        """
        Find item specification by given parameters

        :param name: name of the item
        :type name: string
        :return: item specification
        :rtype: ItemConfiguration
        """
        return self.config.get_by_name(name)

    @logged
    def create_item(self, item_specification):
        """
        Create new item based on specification

        :param item_specification: specification of item
        :type item_specification: ItemConfiguration
        :return: new item
        :rtype: Item
        """
        item = Item(EffectsCollection())

        item.name = item_specification.name
        item.icon = random.choice(item_specification.icons)
        item.cost = item_specification.cost
        item.weight = item_specification.weight
        item.rarity = item_specification.rarity
        item.tags = item_specification.types

        return item

class ItemConfigurations(object):
    """
    Class for configuring items
    """
    logged = Logged()

    def __init__(self):
        """
        Default constructor
        """
        super(ItemConfigurations, self).__init__()
        self.__items = []
        self.__items_by_name = {}

    @logged
    def add_item(self, name, cost, weight, icons, types, rarity):
        """
        Add item to internal configuration
        """
        config = ItemConfiguration(name = name,
                                   cost = cost,
                                   weight = weight,
                                   icons = icons,
                                   types = types,
                                   rarity = rarity)

        self.__add_configuration(config)

    def add_weapon(self, name, cost, weight, icons, types, rarity,
                   damage, critical_range, critical_damage, damage_types,
                   weapon_class):
        """
        Add a weapon to internal configuration
        """
        weapon_config = WeaponConfiguration(damage = damage,
                                            critical_range = critical_range,
                                            critical_damage = critical_damage,
                                            damage_types = damage_types,
                                            weapon_class = weapon_class)

        config = ItemConfiguration(name = name,
                                   cost = cost,
                                   weight = weight,
                                   icons = icons,
                                   types = types,
                                   rarity = rarity,
                                   weapon_configration = weapon_config)

        self.__add_configuration(config)

    def __add_configuration(self, configuration):
        """
        Add configuration to internal lists

        :param configuration: configuration to add
        :type configuration: ItemConfiguration
        """
        self.__items.append(configuration)
        self.__items_by_name[configuration.name] = configuration

    @logged
    def get_all_items(self):
        """
        Returns all items

        :return: list of items
        :rtype: [ItemConfiguration]
        """
        return self.__items

    @logged
    def get_by_name(self, name):
        """
        Retrieve specification of item by name

        :param name: name of the item
        :type name: string
        :return: item specification
        :rtype: ItemConfiguration
        """
        return self.__items_by_name[name]

class ItemConfiguration(object):
    """
    Class representing a single item
    """
    logged = Logged()

    @logged
    def __init__(self, name, cost, weight, icons, types, rarity,
                 weapon_configration = None):
        """
        Default constructor
        """
        self.name = name
        self.cost = cost
        self.weight = weight
        self.icons = icons
        self.types = types
        self.rarity = rarity
        self.weapon_configration = weapon_configration

class WeaponConfiguration(object):
    """
    Class representing weapon configuration
    """
    logged = Logged()

    @logged
    def __init__(self, damage, critical_range, critical_damage, damage_types,
                   weapon_class):
        """
        Default constructor
        """
        self.damage = damage
        self.critical_range = critical_range
        self.critical_damage = critical_damage
        self.damage_types = damage_types
        self.weapon_class = weapon_class

class ItemGenerator(object):
    """
    Class used to generate items
    """

    def __init__(self, tables):
        """
        Default constructor

        :param tables: Tables to use
        """
        self.logger = logging.getLogger('pyherc.generators.item.ItemGenerator')
        self.tables = tables

    def generate_item(self, parameters):
        """
        Generates an item

        :param parameters: parameters guiding generation
        :type parameters: dict
        :returns: generated item
        :rtype: Item
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

        :param parameters: hash table containing parameters for generation
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

        new_item = Item(EffectsCollection())
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
                    new_handle = EffectHandle(trigger = effect_type,
                                       effect = effect['name'],
                                       parameters = None,
                                       charges = 1)

                new_item.add_effect_handle(new_handle)

        if 'appearance' in table.keys():
            new_item.appearance = table['appearance']

        return new_item
