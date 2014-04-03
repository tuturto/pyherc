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
Module for inventory actions
"""
from pyherc.rules import drink, drop_item, equip, pick_up, unequip


class InventoryController():
    """
    Class for inventory actions

    .. versionadded:: 0.9
    """
    def __init__(self, character, action_factory):
        """
        Default constructor
        """
        super().__init__()

        self.character = character
        self.action_factory = action_factory

    def use_item(self, item):
        """
        Use item in different ways, depending on the item
        """
        if item.get_main_type() == 'potion':
            drink(self.character,
                  item,
                  self.action_factory)
        elif item.get_main_type() == 'weapon':
            if self.character.inventory.weapon != None:
                unequip(self.character,
                        self.character.inventory.weapon,
                        self.action_factory)
            equip(self.character,
                  item,
                  self.action_factory)
        elif item.get_main_type() == 'armour':
            if self.character.inventory.armour != None:
                unequip(self.character,
                        self.character.inventory.armour,
                        self.action_factory)
            equip(self.character,
                  item,
                  self.action_factory)
        elif item.get_main_type() == 'ammunition':
            equip(self.character,
                  item,
                  self.action_factory)

    def unequip_item(self, item):
        """
        Unequip item
        """
        unequip(self.character,
                item,
                self.action_factory)

    def pick_up_item(self, item):
        """
        Pick up item
        """
        pick_up(self.character,
                item,
                self.action_factory)

    def drop_item(self, item):
        """
        Drop item
        """
        drop_item(self.character,
                  item,
                  self.action_factory)

    def item_description(self, item):
        """
        Get description of an item
        """
        item_description = item.get_name(self.character,
                                         True)
        if item.weapon_data != None:
            data = item.weapon_data
            item_description += '\ndamage: '
            item_description += ' / '.join((str(x[0]) for x in data.damage))
            item_description += ' ('
            item_description += ' / '.join((str(x[1]) for x in data.damage))
            item_description += ')\n'
        elif item.armour_data != None:
            data = item.armour_data
            item_description += '\ndamage reduction: {0}\n'.format(data.damage_reduction)
            item_description += 'speed modifier: {0}\n'.format(data.speed_modifier)

        item_description += '\n' + item.description

        return item_description
