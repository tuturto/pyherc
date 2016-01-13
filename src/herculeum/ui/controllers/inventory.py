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
Module for inventory actions
"""
from pyherc.data import (is_potion, is_weapon, is_armour, is_ammunition,
                         is_trap_bag, is_boots)
from pyherc.ports import (drink, is_drinking_legal, place_trap,
                          drop_item, equip, pick_up, unequip)


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
        self.action_factory = action_factory # TODO: not needed anymore

    def use_item(self, item):
        """
        Use item in different ways, depending on the item
        """
        if is_potion(item) and is_drinking_legal(self.character, item):
            drink(self.character,
                  item)
        elif is_weapon(item):
            if self.character.inventory.weapon is not None:
                unequip(self.character,
                        self.character.inventory.weapons)
            equip(self.character,
                  item)
        elif is_armour(item):
            if self.character.inventory.armour is not None:
                unequip(self.character,
                        self.character.inventory.armour)
            equip(self.character,
                  item)
        elif is_boots(item):
            if self.character.inventory.boots is not None:
                unequip(self.character,
                        self.character.inventory.boots)
            equip(self.character,
                  item)
        elif is_ammunition(item):
            equip(self.character,
                  item)
        elif is_trap_bag(item):
            place_trap(self.character,
                       item)


    def unequip_item(self, item):
        """
        Unequip item
        """
        unequip(self.character,
                item)

    def pick_up_item(self, item):
        """
        Pick up item
        """
        pick_up(self.character,
                item)

    def drop_item(self, item):
        """
        Drop item
        """
        drop_item(self.character,
                  item)

    def item_description(self, item):
        """
        Get description of an item
        """
        item_description = item.get_name(self.character,
                                         True)
        if item.weapon_data is not None:
            data = item.weapon_data
            item_description += '\ndamage: '
            item_description += ' / '.join((str(x[0]) for x in data.damage))
            item_description += ' ('
            item_description += ' / '.join((str(x[1]) for x in data.damage))
            item_description += ')\n'
        elif item.armour_data is not None:
            data = item.armour_data
            item_description += '\ndamage reduction: {0}\n'.format(data.damage_reduction)
            item_description += 'speed modifier: {0}\n'.format(data.speed_modifier)

        item_description += '\n' + item.description

        return item_description
