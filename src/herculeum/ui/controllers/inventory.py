#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
Module for inventory actions
"""
class InventoryController(object):
    """
    Class for inventory actions

    .. versionadded:: 0.9
    """
    def __init__(self, character, action_factory):
        """
        Default constructor
        """
        super(InventoryController, self).__init__()

        self.character = character
        self.action_factory = action_factory

    def use_item(self, item):
        """
        Use item in different ways, depending on the item
        """
        if item.get_main_type() == 'potion':
            self.character.drink(item, self.action_factory)
        elif item.get_main_type() == 'weapon':
            if self.character.inventory.weapon != None:
                self.character.unequip(self.character.inventory.weapon,
                                       self.action_factory)
            self.character.equip(item,
                                 self.action_factory)
        elif item.get_main_type() == 'armour':
            if self.character.inventory.armour != None:
                self.character.unequip(self.character.inventory.armour,
                                       self.action_factory)
            self.character.equip(item,
                                 self.action_factory)
        elif item.get_main_type() == 'ammunition':
            self.character.equip(item,
                                 self.action_factory)

    def unequip_item(self, item):
        """
        Unequip item
        """
        self.character.unequip(item,
                               self.action_factory)

    def pick_up_item(self, item):
        """
        Pick up item
        """
        self.character.pick_up(item, self.action_factory)

    def drop_item(self, item):
        """
        Drop item
        """
        self.character.drop_item(item, self.action_factory)
