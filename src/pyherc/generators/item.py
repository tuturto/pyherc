# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Classes needed for item generation
"""

import random

import pyherc
from pyherc.aspects import log_debug, log_info
from pyherc.data import Item
from pyherc.data.effects import EffectHandle, EffectsCollection
from pyherc.data.item import (AmmunitionData, ArmourData, WeaponData, TrapData,
                              BootsData)


class ItemGenerator():
    """
    Class used to generate items
    """
    @log_debug
    def __init__(self, config):
        """
        Default constructor

        :param config: configuration for items
        :type config: ItemConfiguration
        """
        super().__init__()
        self.config = config

    @log_info
    def generate_item(self, name=None, item_type=None, artefact_type=None):
        """
        Generate an item

        :param name: name of the item to generate
        :type name: string
        :param item_type: type of the item to generate
        :type item_type: string
        :return: Generated item
        :rtype: Item
        """
        if artefact_type:
            return pyherc.vtable['\ufdd0:generate-artefact'](artefact_type)
        else:        
            item_specification = self.find_item_specification(name=name,
                                                              item_type=item_type)

            item = self.create_item(item_specification)

            return item

    @log_debug
    def find_item_specification(self, name=None, item_type=None):
        """
        Find item specification by given parameters

        :param name: name of the item
        :type name: string
        :param item_type: type of the item to generate
        :type item_type: string
        :return: item specification
        :rtype: ItemConfiguration
        """
        if name is not None:
            return self.config.get_by_name(name)
        else:
            return self.config.get_by_type(item_type)

    @log_debug
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
        item.description = item_specification.description
        item.icon = random.choice(item_specification.icons)
        item.cost = item_specification.cost
        item.weight = item_specification.weight
        item.rarity = item_specification.rarity
        item.tags = item_specification.types

        if not item_specification.weapon_configration is None:
            weapon_spec = item_specification.weapon_configration
            damage = []
            damage.extend(weapon_spec.damage)
            item.weapon_data = WeaponData(
                damage=(damage),
                critical_range=weapon_spec.critical_range,
                critical_damage=weapon_spec.critical_damage,
                weapon_type=weapon_spec.weapon_class,
                ammunition_type=weapon_spec.ammunition_type,
                speed=weapon_spec.speed)

        if item_specification.armour_configuration is not None:
            armour_spec = item_specification.armour_configuration
            item.armour_data = ArmourData(
                damage_reduction=armour_spec.damage_reduction,
                speed_modifier=armour_spec.speed_modifier)

        if item_specification.ammunition_configuration is not None:
            ammo_spec = item_specification.ammunition_configuration
            item.ammunition_data = AmmunitionData(
                damage=ammo_spec.damage,
                critical_range=ammo_spec.critical_range,
                critical_damage=ammo_spec.critical_damage,
                ammunition_type=ammo_spec.ammunition_type,
                count=ammo_spec.count)

        if item_specification.trap_configuration is not None:
            trap_spec = item_specification.trap_configuration
            item.trap_data = TrapData(
                trap_name = trap_spec.name,
                count = trap_spec.count)

        if item_specification.boots_configuration is not None:
            boots_spec = item_specification.boots_configuration
            item.boots_data = BootsData(
                damage_reduction = boots_spec.damage_reduction,
                speed_modifier = boots_spec.speed_modifier)

        for spec in item_specification.effect_handles:
            new_handle = EffectHandle(trigger=spec.trigger,
                                      effect=spec.effect,
                                      parameters=spec.parameters,
                                      charges=spec.charges)

            item.add_effect_handle(new_handle)

        for effect in item_specification.effects:
            item.add_effect(effect) # TODO: do not use same instance

        return item


class ItemConfigurations():
    """
    Class for configuring items
    """
    @log_debug
    def __init__(self, rng):
        """
        Default constructor

        :param rng: random number generator
        :type rng: Random
        """
        super().__init__()
        self.__items = []
        self.__items_by_name = {}
        self.rng = rng

    @log_debug
    def add_item(self, item_config):
        """
        Add item to internal configuration
        """
        self.__items.append(item_config)
        self.__items_by_name[item_config.name] = item_config

    @log_debug
    def get_all_items(self):
        """
        Returns all items

        :return: list of items
        :rtype: [ItemConfiguration]
        """
        return self.__items

    @log_debug
    def get_by_name(self, name):
        """
        Retrieve specification of item by name

        :param name: name of the item
        :type name: string
        :return: item specification
        :rtype: ItemConfiguration
        """
        return self.__items_by_name[name]

    @log_debug
    def get_by_type(self, item_type):
        """
        Retrieve a random specification of item by type

        :param item_type: type of the item
        :type item_type: string
        :return: item specification
        :rtype: ItemConfiguration
        """
        matching_specs = [x for x in self.__items
                          if item_type in x.types]

        max_score = sum([x.rarity for x in matching_specs])

        score = self.rng.randint(1, max_score)
        current_score = 0

        for spec in matching_specs:
            current_score = current_score + spec.rarity
            if current_score >= score:
                return spec

        return None


class ItemConfiguration():
    """
    Class representing a single item
    """
    rarities = {'artifact': 1,
                'legendary': 4,
                'epic': 16,
                'rare': 64,
                'uncommon': 256,
                'common': 1024}

    @log_debug
    def __init__(self, name, cost, weight, icons, types, rarity,
                 weapon_configration=None, effect_handles=None,
                 effects=None, armour_configuration=None,
                 ammunition_configuration=None, trap_configuration=None,
                 boots_configuration=None, description=''):
        """
        Default constructor
        """
        super().__init__()
        self.name = name
        self.description = description
        self.cost = cost
        self.weight = weight
        self.icons = icons
        self.types = types
        self.rarity = self.rarities[rarity]
        self.weapon_configration = weapon_configration
        self.armour_configuration = armour_configuration
        self.ammunition_configuration = ammunition_configuration
        self.trap_configuration = trap_configuration
        self.boots_configuration = boots_configuration

        if effect_handles is None:
            self.effect_handles = []
        else:
            self.effect_handles = effect_handles

        if effects is None:
            self.effects = []
        else:
            self.effects = effects


class WeaponConfiguration():
    """
    Class representing weapon configuration
    """
    @log_debug
    def __init__(self, damage, critical_range, critical_damage, weapon_class,
                 ammunition_type=None, speed=1):
        """
        Default constructor
        """
        super().__init__()

        self.damage = damage
        self.critical_range = critical_range
        self.critical_damage = critical_damage
        self.weapon_class = weapon_class
        self.ammunition_type = ammunition_type
        self.speed = speed


class BootsConfiguration():
    """
    Class for configuring boots
    """
    @log_debug
    def __init__(self, damage_reduction, speed_modifier):
        """"
        Default initializer
        """
        super().__init__()

        self.damage_reduction = damage_reduction
        self.speed_modifier = speed_modifier


class ArmourConfiguration():
    """
    Class representing armour configuration
    """
    @log_debug
    def __init__(self, damage_reduction, speed_modifier):
        """
        Default constructor
        """
        super().__init__()

        self.damage_reduction = damage_reduction
        self.speed_modifier = speed_modifier


class AmmunitionConfiguration():
    """
    Class representing ammunition configuration

    .. versionadded:: 0.8
    """
    @log_debug
    def __init__(self, damage, critical_range, critical_damage,
                 ammunition_type, count):
        """
        Default constructor
        """
        super().__init__()

        self.damage = damage
        self.critical_range = critical_range
        self.critical_damage = critical_damage
        self.ammunition_type = ammunition_type
        self.count = count


class TrapConfiguration():
    """
    Class representing trap configuration
    """
    @log_debug
    def __init__(self, name, count):
        """
        Default constructor
        """
        super().__init__()

        self.name = name
        self.count = count
