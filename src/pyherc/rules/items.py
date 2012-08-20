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
Rules for manipulating items

.. warning:: This code will be eventually replaced by action sub system
"""

import logging
import pyherc.rules.magic

logger = logging.getLogger('pyherc.rules.items')

def drop(model, character, item):
    """
    Drop item from inventory
    :param model: model to use
    :type model: Model
    :param character: character who is dropping the item
    :type character: Character
    :param item: item to be dropped
    :type item: Item

    .. warning:: This code will be eventually replaced by action sub system
    """
    assert(not model == None)
    assert(not character == None)
    assert(not item == None)
    assert(item in character.inventory)

    if(item in character.weapons):
        unwield(model, character, item, instant = True)

    character.level.add_item(item, character.location)
    character.inventory.remove(item)
    character.add_to_tick(1.5)

def wield(model, character, item, dual_wield = False):
    """
    Wield a weapon
    :param model: model to use
    :type model: Model
    :param character: character trying to wield the weapon
    :type character: Character
    :param item: weapon to wield
    :type item: Item
    :param dual_wield: should character perform dual wield
    :type dual_wield: Boolean

    .. warning:: This code will be eventually replaced by action sub system
    """

    if len(character.weapons) == 0:
        #simple wield
        character.weapons.append(item)
    else:
        #possible dual wield?
        if dual_wield == True:
            if len(character.weapons) == 1:
                if can_dual_wield(model, character, character.weapons[0], item):
                    character.weapons.append(item)

def can_dual_wield(model, character, item1, item2):
    """
    Checks if character can dual-wield given items

    :param model: model to use
    :type model: Model
    :param character: character to try dual-wielding
    :type character: Character
    :param item1: item to wield
    :type item1: Item
    :param item2: item to wield
    :type item2: Item
    :returns: 1 if can dual-wield, 0 otherwise
    :rtype: integer

    .. warning:: This code will be eventually replaced by action sub system
    """
    if (is_dual_wieldable(model, character, item1)
            and is_dual_wieldable(model, character, item2)):

        return 1
    else:
        return 0

def is_dual_wieldable(model, character, item):
    """
    Checks if item is dual-wieldable for a character

    :param model: model to use
    :type model: Model
    :param character: character to try dual-wielding
    :type character: Character
    :param item: item to dual wield
    :type item: Item
    :returns: 1 if can dual-wield, 0 otherwise
    :rtype: integer

    .. warning:: This code will be eventually replaced by action sub system
    """
    assert model != None
    assert character != None
    assert item != None

    if item.weapon_data != None:
        if (('one-handed weapon' in item.get_tags()
            or 'light weapon' in item.get_tags())):
            return 1
        else:
            return 0
    else:
        #mundane items can not be dual-wielded
        return 0

def unwield(model, character, item, instant = False):
    """
    Unwield an item

    :param model: model to use
    :type model: Model
    :param character: character unwielding an item
    :type character: Character
    :param item: item to unwield
    :type item: Item
    :param instant: is this instant action, default False
    :type instant: Boolean
    :returns: True if unwield was succesfull, False otherwise
    :rtype: Boolean

    .. warning:: This code will be eventually replaced by action sub system
    """
    character.weapons.remove(item)

    return True
