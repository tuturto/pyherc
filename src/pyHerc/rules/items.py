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
import pyHerc.rules.magic
import time

__logger = logging.getLogger('pyHerc.rules.items')

def pick_up(model, character, item):
    """
    Pick up an item
    @param model: model to use
    @param character: character picking up the item
    @param item: item to be picked up
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
    model.raise_event(event)

    character.level.items.remove(item)
    character.inventory.append(item)
    item.location = ()
    character.tick = time.getNewTick(character, 1.5)

    __logger.debug('item picked up')

def drop(model, character, item):
    """
    Drop item from inventory
    @param model: model to use
    @param character: character who is dropping the item
    @param item: item to be dropped
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
    model.raise_event(event)

    if(item in character.weapons):
        unwield(model, character, item, instant = True)

    character.level.addItem(item, character.location)
    character.inventory.remove(item)
    character.tick = time.getNewTick(character, 1.5)

    __logger.debug('item dropped')

def wield(model, character, item, dualWield = False):
    """
    Wield a weapon
    @param model: model to use
    @param character: character trying to wield the weapon
    @param item: weapon to wield
    @param dualWield: should character perform dual wield
    """
    __logger.debug(character.__str__() + ' wielding item ' + item.__str__())

    if len(character.weapons) == 0:
        #simple wield
        character.weapons.append(item)
        __logger.debug(character.__str__() + ' wielded item ' + item.__str__())
        event = {}
        event['type'] = 'item'
        event['wield'] = 1
        event['character'] = character
        event['item'] = item
        event['location'] = character.location
        event['level'] = character.level
        event['proficient'] = character.is_proficient(item)
        model.raise_event(event)
    else:
        #possible dual wield?
        if dualWield == True:
            if len(character.weapons) == 1:
                if can_dual_wield(model, character, character.weapons[0], item):
                    character.weapons.append(item)
                    __logger.debug(character.__str__() + ' dual-wielded item ' + item.__str__())
                    event = {}
                    event['type'] = 'item'
                    event['wield'] = 1
                    event['character'] = character
                    event['item'] = item
                    event['location'] = character.location
                    event['level'] = character.level
                    event['proficient'] = character.is_proficient(item)
                    model.raise_event(event)
                    #TODO: feedback when wielding is not possible

def can_dual_wield(model, character, item1, item2):
    """
    Checks if character can dual-wield given items
    @param model: model to use
    @param character: character to try dual-wielding
    @param item1: item to wield
    @param item2: item to wield
    @return: 1 if can dual-wield, 0 otherwise
    """
    if is_dual_wieldable(model, character, item1) and is_dual_wieldable(model, character, item2):
        return 1
    else:
        return 0

def is_dual_wieldable(model, character, item):
    """
    Checks if item is dual-wieldable for a character
    @param model: model to use
    @param character: character to try dual-wielding
    @param item: item to dual wield
    @return: 1 if can dual-wield, 0 otherwise
    """
    if hasattr(item, 'tags'):
        if ('one-handed weapon' in item.tags or 'light weapon' in item.tags):
            return 1
        else:
            return 0
    else:
        #mundane items can not be dual-wielded
        return 0

def unwield(model, character, item, instant = False):
    '''
    Unwield an item
    @param model: model to use
    @param character: character unwielding an item
    @param item: item to unwield
    @param instant: is this instant action, default False
    @return: True if unwield was succesfull, False otherwise
    '''
    __logger.debug(character.__str__() + ' unwielding ' + item.__str__())

    character.weapons.remove(item)

    event = {}
    event['type'] = 'item'
    event['unwield'] = 1
    event['character'] = character
    event['item'] = item
    event['location'] = character.location
    event['level'] = character.level
    model.raise_event(event)

    return True

    __logger.debug(character.__str__() + ' unwielded ' + item.__str__())

def drink_potion(model, character, potion, dice = None):
    """
    Drink a potion
    @param model: model to use
    @param character: character drinking a potion
    @param potion: potion to drink
    @param dice: optional prerolled dice
    """
    __logger.debug(character.__str__() + ' drinking ' + potion.__str__())

    assert(model != None)
    assert(character != None)
    assert(potion != None)
    assert(potion in character.inventory)

    if potion.charges < 1:
        __logger.warning('no charges left!')
        #out of charges
        #TODO: feed back
        return 0

    potion.charges = potion.charges - 1

    #drinking a potion usually identifies it
    character.identify_item(potion)

    if hasattr(potion, 'effects'):
        for effect in potion.effects['on drink']:
            pyHerc.rules.magic.castEffect(model, character, effect, dice)

    if potion.charges < 1:
        character.inventory.remove(potion)

    #TODO: raise event
    __logger.debug(character.__str__() + ' drank ' + potion.__str__())

