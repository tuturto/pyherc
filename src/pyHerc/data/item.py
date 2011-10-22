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

class Item:
    """
    Represents item
    """

    def __init__(self):
        #attributes
        self.name = 'prototype'
        self.questItem = 0
        #location
        self.location = ()
        #icon
        self.icon = None
        self.weaponData = None

    def __str__(self):
        return self.name

    def get_name(self, character, decorate = False):
        """
        Get name of the item
        Name can be appearance or given name
        @param character: character handling the item
        @param decorate: should name be decorated with status info, default False
        """
        assert character != None

        if hasattr(self, 'appearance'):
            if self.name in character.itemMemory.keys():
                name = character.itemMemory[self.name]
            else:
                name = self.appearance
        else:
            name = self.name

        if decorate == True:
            if self in character.weapons:
                name = name + ' (weapon in hand)'

        return name

class WeaponData:
    '''
    Class representing weapon data of items
    '''
    def __init__(self, damage = None, damage_type = None, critical_range = None,
                 critical_damage = None, weapon_type = None, tags = None):

        self.damage = damage
        self.damage_type = damage_type
        self.critical_range = critical_range
        self.critical_damage = critical_damage
        self.weapon_type = weapon_type
        self.tags = tags
