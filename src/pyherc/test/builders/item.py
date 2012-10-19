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
Module for item builder
"""
from pyherc.data import Item
from pyherc.data.effects import EffectsCollection
from pyherc.data.item import WeaponData

class ItemBuilder(object):
    """
    Class for building Items
    """
    def __init__(self):
        """
        Default constructor
        """
        super(ItemBuilder, self).__init__()
        self.name = 'prototype'
        self.appearance = ''
        self.effect_handles = []
        self.location = ()
        self.icon = 0
        self.weapon_data = None
        self.tags = []

    def with_name(self, name):
        self.name = name
        return self

    def with_appearance(self, appearance):
        self.appearance = appearance
        return self

    def with_effect(self, handle):
        if hasattr(handle, 'build'):
            self.effect_handles.append(handle.build())
        else:
            self.effect_handles.append(handle)
        return self

    def with_location(self, location):
        self.location = location
        return self

    def with_icon(self, icon):
        self.icon = icon
        return self

    def with_damage(self, damage, damage_type):
        if self.weapon_data == None:
            self.weapon_data = WeaponData()
        self.weapon_data.damage = damage
        self.weapon_data.damage_types = [damage_type]
        return self

    def with_tag(self, tag):
        self.tags.append(tag)
        return self

    def with_weapon_type(self, weapon_type):
        if self.weapon_data == None:
            self.weapon_data = WeaponData()
        self.weapon_data.weapon_type = weapon_type
        return self

    def build(self):
        """
        Build item

        Returns:
            Item
        """
        item = Item(effects_collection = EffectsCollection())

        item.name = self.name
        item.appearance = self.appearance
        item.location = self.location
        item.icon = self.icon
        if self.weapon_data != None:
            item.weapon_data = self.weapon_data

        for handle in self.effect_handles:
            item.add_effect_handle(handle)

        item.tags = self.tags

        return item
