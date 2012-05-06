#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2011 Tuukka Turto
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
Module for item related classes

Classes:
    Item
    WeaponData
    EffectHandle
"""

import collections

class Item(object):
    """
    Represents item
    """

    def __init__(self):
        super(Item, self).__init__()
        #attributes
        self.name = 'prototype'
        self.appearance = ''
        self.quest_item = 0
        #location
        self.location = ()
        self.level = None
        #icon
        self.icon = None
        self.weapon_data = None
        self.effects = {}
        self.weight = None
        self.rarity = None
        self.cost = None
        self.tags = {}

    def __str__(self):
        return self.name

    def get_name(self, character, decorate = False):
        """
        Get name of the item
        Name can be appearance or given name

        Args:
            character: character handling the item
            decorate: should name be decorated with status info, default False
        """
        assert character != None

        if self.appearance != '':
            if self.name in character.item_memory.keys():
                name = character.item_memory[self.name]
            else:
                name = self.appearance
        else:
            name = self.name

        if decorate == True:
            if self in character.weapons:
                name = name + ' (weapon in hand)'

        return name

    def add_effect(self, effect):
        """
        Adds an effect to an item

        Args:
            effect: effect to add
        """
        if self.effects == None:
            self.effects = {}

        if self.effects.has_key(effect.trigger):
            self.effects[effect.trigger].append(effect)
        else:
            self.effects[effect.trigger] = [effect]

    def get_effects(self, effect_type = None):
        """
        Retrieves effects the item has

        Args:
            effect_type: type of effects retrieved. Default None

        Returns:
            list of effects
        """
        effect_list = []

        if self.effects != None:
            if effect_type == None:
                for trigger in self.effects.values():
                    effect_list = effect_list + trigger
            else:
                if self.effects.has_key(effect_type):
                    effect_list = effect_list + self.effects[effect_type]
                else:
                    effect_list = []

        return effect_list

    def __get_charges_left(self):
        """
        Returns list containing amount of charges left in item
        """
        if self.effects == None:
            return []

        effect_list = self.get_effects()

        return [x.charges for x in effect_list]

    def __get_maximum_charges_left(self):
        """
        Return highest amount of charges left in item
        """
        charges = self.charges_left

        if charges != None:
            if isinstance(charges, collections.Sequence):
                if len(charges) > 0:
                    return max(charges)
                else:
                    return None
            else:
                return charges
        else:
            return None

    def __get_minimum_charges_left(self):
        """
        Return smallest amount of charges left in item
        """
        charges = self.charges_left

        if charges != None:
            return min(charges)
        else:
            return None

    charges_left = property(__get_charges_left)
    maximum_charges_left = property(__get_maximum_charges_left)
    minimum_charges_left = property(__get_minimum_charges_left)

    def get_main_type(self):
        """
        Return main type of the item
        """
        main_type = 'undefined'

        if 'weapon' in self.tags:
            main_type = 'weapon'
        elif 'potion' in self.tags:
            main_type = 'potion'
        elif 'food' in self.tags:
            main_type = 'food'

        return main_type

    def get_tags(self):
        """
        Return tags
        """
        return self.tags

class WeaponData(object):
    """
    Class representing weapon data of items
    """
    def __init__(self, damage = None, damage_type = None, critical_range = None,
                 critical_damage = None, weapon_type = None):

        self.damage = damage
        self.damage_type = damage_type
        self.critical_range = critical_range
        self.critical_damage = critical_damage
        self.weapon_type = weapon_type
