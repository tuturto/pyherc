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

import os, sys
import logging
import pyHerc.data.model
import time

__logger = logging.getLogger('pyHerc.rules.items')

def pickUp(model, character, item):
    """
    Pick up an item
    Parameters:
        model : model to use
        character : character picking up the item
        item : item to be picked up
    """
    assert(not model == None)
    assert(not character == None)
    assert(not item == None)
    assert(item in character.level.items)

    __logger.debug(character.__str__() + ' picking up item: ' + item.__str__())

    event = {}
    event['type'] = 'item'
    event['pick up'] = 1
    event['character'] = character
    event['item'] = item
    event['location'] = character.location
    event['level'] = character.level
    model.raiseEvent(event)

    character.level.items.remove(item)
    character.inventory.append(item)
    item.location = ()
    character.tick = time.getNewTick(character, 1.5)

    __logger.debug('item picked up')

def drop(model, character, item):
    """
    Drop item from inventory
    Parameters:
        model : model to use
        character : character who is dropping the item
        item : item to be dropped
    """
    assert(not model == None)
    assert(not character == None)
    assert(not item == None)
    assert(item in character.inventory)

    __logger.debug(character.__str__() + ' dropping item ' + item.__str__())

    event = {}
    event['type'] = 'item'
    event['drop'] = 1
    event['character'] = character
    event['item'] = item
    event['location'] = character.location
    event['level'] = character.level
    model.raiseEvent(event)

    character.level.addItem(item, character.location)
    character.inventory.remove(item)
    character.tick = time.getNewTick(character, 1.5)

    __logger.debug('item dropped')

def wield(model, character, item, dualWield = False):
    """
    Wield a weapon
    Parameters:
        model : model to use
        character : character trying to wield the weapon
        item : weapon to wield
        dualWield : should character perform dual wield
    """
    __logger.debug(character.__str__() + ' wielding item ' + item.__str__())

    if len(character.weapons) == 0:
        #simple wield
        character.weapons.append(item)
    else:
        #possible dual wield?
        if dualWield == True:
            if len(character.weapons) == 1:
                character.weapons.append(item)
