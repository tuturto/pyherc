# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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
Module for item builder
"""
from pyherc.data import Item
from pyherc.data.effects import EffectsCollection
from pyherc.data.item import WeaponData, ArmourData, AmmunitionData


class ItemBuilder():
    """
    Class for building Items
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.name = 'prototype'
        self.appearance = ''
        self.effect_handles = []
        self.location = ()
        self.icon = 0
        self.weapon_data = None
        self.armour_data = None
        self.ammunition_data = None
        self.tags = []

    def with_name(self, name):
        """
        Configure name of the item

        :param name: name of the item
        :type name: string
        """
        self.name = name
        return self

    def with_appearance(self, appearance):
        """
        Configure appearance of the item

        :param appearance: appearance of the item
        :type appearance: string

        .. note:: appearance is used as a name of the item if it is not
                  familiar to the person inspecting it
        """
        self.appearance = appearance
        return self

    def with_effect(self, handle):
        """
        Add effect handle to the item

        :param handle: effect handle to add
        :type handle: {}

        .. note:: can be called multiple times
        """
        if hasattr(handle, 'build'):
            self.effect_handles.append(handle.build())
        else:
            self.effect_handles.append(handle)
        return self

    def with_location(self, location):
        """
        Configure location of the item

        :param location: location of the item
        :type location: (int, int)
        """
        self.location = location
        return self

    def with_icon(self, icon):
        """
        Configure icon of the item

        :param icon: icon to use
        :type icon: int
        """
        self.icon = icon
        return self

    def with_damage(self, damage, damage_type):
        """
        Configure amount of damage done if used as weapon

        :param damage: amount of damage
        :type damage: int
        :param damage_type:
        """
        if self.weapon_data is None:
            self.weapon_data = WeaponData()
        self.weapon_data.damage.append((damage, damage_type))
        return self

    def with_required_ammunition_type(self, ammunition_type):
        """
        Configure type of ammunition this weapon requires

        :param ammunition_type: type of ammunition this weapon requires
        :type ammunition_type: string
        """
        if self.weapon_data is None:
            self.weapon_data = WeaponData()
        self.weapon_data.ammunition_type = ammunition_type
        return self

    def with_ammunition_type(self, ammunition_type):
        """
        Configure type of this ammunition

        :param ammunition_type: type of ammunition
        :type ammunition_type: string
        """
        if self.ammunition_data is None:
            self.ammunition_data = AmmunitionData()
        self.ammunition_data.ammunition_type = ammunition_type
        return self

    def with_range_damage(self, damage, damage_type):
        """
        Configure damage of this ammunition

        :param damage: amount of damage
        :type damage: int
        :param damage_type: type of damage
        :type damage_type: string

        .. note:: can be called multiple times
        """
        if self.ammunition_data is None:
            self.ammunition_data = AmmunitionData()
        self.ammunition_data.damage.append((damage, damage_type))
        return self

    def with_count(self, count):
        """
        Configure amount of itmes in countable stack

        :param count: amount of items
        :type count: int
        """
        if self.ammunition_data is None:
            self.ammunition_data = AmmunitionData()
        self.ammunition_data.count = count
        return self

    def with_tag(self, tag):
        """
        Add tag to the item

        :param tag: tag to add
        :type tag: string

        .. note:: this can be called multiple times
        """
        self.tags.append(tag)
        return self

    def with_weapon_type(self, weapon_type):
        """
        Set weapon type of the item

        :param weapon_type: type of weapon
        :type weapon_type: string
        """
        if self.weapon_data is None:
            self.weapon_data = WeaponData()
        self.weapon_data.weapon_type = weapon_type
        return self

    def with_damage_reduction(self, damage_reduction):
        """
        Set damage reduction of the item

        :param damage_reduction: amount of damage reduction
        :type damage_reduction: int
        """
        if self.armour_data is None:
            self.armour_data = ArmourData()
        self.armour_data.damage_reduction = damage_reduction
        return self

    def with_speed(self, speed):
        """
        Set speed modifier of the item if used as a weapon

        :param speed: speed modifier to use
        :type speed: double
        """
        if self.weapon_data is None:
            self.weapon_data = WeaponData()
        self.weapon_data.speed = speed
        return self

    def with_speed_modifier(self, speed_modifier):
        """
        Set speed modifier of the item if used as an armour

        :param speed_modifier: speed modifier to use
        :type speed_modifier: double
        """
        if self.armour_data is None:
            self.armour_data = ArmourData()
        self.armour_data.speed_modifier = speed_modifier
        return self

    def build(self):
        """
        Build item

        Returns:
            Item
        """
        item = Item(effects_collection=EffectsCollection())

        item.name = self.name
        item.appearance = self.appearance
        item.location = self.location
        item.icon = self.icon
        item.tags = self.tags

        if self.weapon_data is not None:
            item.weapon_data = self.weapon_data
            item.tags.append('weapon')

        if self.armour_data is not None:
            item.armour_data = self.armour_data
            item.tags.append('armour')

        if self.ammunition_data is not None:
            item.ammunition_data = self.ammunition_data
            item.tags.append('ammunition')

        for handle in self.effect_handles:
            item.add_effect_handle(handle)

        return item
