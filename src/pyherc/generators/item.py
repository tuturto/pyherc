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

import random
from pyherc.data import Item
from pyherc.data.item import WeaponData
from pyherc.data.effects import EffectsCollection, EffectHandle
from pyherc.aspects import Logged

class ItemGenerator(object):
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
        super(ItemGenerator, self).__init__()
        self.config = config

    @logged
    def generate_item(self, name = None, item_type = None):
        """
        Generate an item

        :param name: name of the item to generate
        :type name: string
        :param item_type: type of the item to generate
        :type item_type: string
        :return: Generated item
        :rtype: Item
        """
        item_specification = self.find_item_specification(name = name,
                                                          item_type = item_type)

        item = self.create_item(item_specification)

        return item

    @logged
    def find_item_specification(self, name = None, item_type = None):
        """
        Find item specification by given parameters

        :param name: name of the item
        :type name: string
        :param item_type: type of the item to generate
        :type item_type: string
        :return: item specification
        :rtype: ItemConfiguration
        """
        if not name is None:
            return self.config.get_by_name(name)
        else:
            return self.config.get_by_type(item_type)

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

        if not item_specification.weapon_configration is None:
            weapon_spec = item_specification.weapon_configration
            item.weapon_data = WeaponData(
                                    damage = weapon_spec.damage,
                                    critical_range = weapon_spec.critical_range,
                                    critical_damage = weapon_spec.critical_damage,
                                    damage_types = weapon_spec.damage_types,
                                    weapon_type = weapon_spec.weapon_class)

        for spec in item_specification.effect_handles:
            new_handle = EffectHandle(trigger = spec.trigger,
                                       effect = spec.effect,
                                       parameters = spec.parameters,
                                       charges = spec.charges)

            item.add_effect_handle(new_handle)

        return item

class ItemConfigurations(object):
    """
    Class for configuring items
    """
    logged = Logged()

    def __init__(self, rng):
        """
        Default constructor

        :param rng: random number generator
        :type rng: Random
        """
        super(ItemConfigurations, self).__init__()
        self.__items = []
        self.__items_by_name = {}
        self.rng = rng

    @logged
    def add_item(self, item_config):
        """
        Add item to internal configuration
        """
        self.__items.append(item_config)
        self.__items_by_name[item_config.name] = item_config

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

    @logged
    def get_by_type(self, item_type):
        """
        Retrieve a random specification of item by type

        :param item_type: type of the item
        :type item_type: string
        :return: item specification
        :rtype: ItemConfiguration
        """
        matching_specs = filter(lambda x: item_type in x.types,
                                self.__items)

        max_score = reduce(lambda x, y: x + y.rarity,
                           matching_specs, 0)

        score = self.rng.randint(1, max_score)
        current_score = 0

        for spec in matching_specs:
            current_score = current_score + spec.rarity
            if current_score >= score:
                return spec

        return None

class ItemConfiguration(object):
    """
    Class representing a single item
    """
    logged = Logged()

    rarities = {'artifact': 1,
                'legendary': 4,
                'epic': 16,
                'rare': 64,
                'uncommon': 256,
                'common': 1024}

    @logged
    def __init__(self, name, cost, weight, icons, types, rarity,
                 weapon_configration = None, effect_handles = None):
        """
        Default constructor
        """
        self.name = name
        self.cost = cost
        self.weight = weight
        self.icons = icons
        self.types = types
        self.rarity = self.rarities[rarity]
        self.weapon_configration = weapon_configration

        if effect_handles is None:
            self.effect_handles = []
        else:
            self.effect_handles = effect_handles

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
