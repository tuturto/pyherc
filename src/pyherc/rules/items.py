#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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
"""

import logging
import pyherc.data.model
import pyherc.rules.magic
import pyherc.rules.time

logger = logging.getLogger('pyherc.rules.items')

def pick_up(model, character, item):
    """
    Pick up an item

    Args:
        model: model to use
        character: character picking up the item
        item: item to be picked up
    """
    assert(not model == None)
    assert(not character == None)
    assert(not item == None)
    assert(item in character.level.items)

    logger.debug(character.__str__() + ' picking up item: ' + item.__str__())

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
    character.tick = pyherc.rules.time.get_new_tick(character, 1.5)

    logger.debug('item picked up')

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

    logger.debug('{0} dropping item {1}'.format(character, item))

    if(item in character.weapons):
        unwield(model, character, item, instant = True)

    character.level.add_item(item, character.location)
    character.inventory.remove(item)
    character.tick = pyherc.rules.time.get_new_tick(character, 1.5)

    event = {}
    event['type'] = 'item'
    event['drop'] = 1
    event['character'] = character
    event['item'] = item
    event['location'] = character.location
    event['level'] = character.level
    model.raise_event(event)

    logger.debug('item dropped')

def wield(model, character, item, dual_wield = False):
    """
    Wield a weapon
    @param model: model to use
    @param character: character trying to wield the weapon
    @param item: weapon to wield
    @param dual_wield: should character perform dual wield
    """
    logger.debug(character.__str__() + ' wielding item ' + item.__str__())

    if len(character.weapons) == 0:
        #simple wield
        character.weapons.append(item)
        logger.debug(character.__str__() + ' wielded item ' + item.__str__())
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
        if dual_wield == True:
            if len(character.weapons) == 1:
                if can_dual_wield(model, character, character.weapons[0], item):
                    character.weapons.append(item)
                    logger.debug('{0} dual-wielded item {1}'.format(
                                                    character, item))
                    event = {}
                    event['type'] = 'item'
                    event['wield'] = 1
                    event['character'] = character
                    event['item'] = item
                    event['location'] = character.location
                    event['level'] = character.level
                    event['proficient'] = character.is_proficient(item)
                    model.raise_event(event)

def can_dual_wield(model, character, item1, item2):
    """
    Checks if character can dual-wield given items
    @param model: model to use
    @param character: character to try dual-wielding
    @param item1: item to wield
    @param item2: item to wield
    @return: 1 if can dual-wield, 0 otherwise
    """
    if (is_dual_wieldable(model, character, item1)
            and is_dual_wieldable(model, character, item2)):

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
    '''
    Unwield an item
    @param model: model to use
    @param character: character unwielding an item
    @param item: item to unwield
    @param instant: is this instant action, default False
    @return: True if unwield was succesfull, False otherwise
    '''
    logger.debug('{0} unwielding {1}'.format(character, item))

    character.weapons.remove(item)

    event = {}
    event['type'] = 'item'
    event['unwield'] = 1
    event['character'] = character
    event['item'] = item
    event['location'] = character.location
    event['level'] = character.level
    model.raise_event(event)

    logger.debug('{0} unwielded {1}'.format(character, item))

    return True

def drink_potion(model, character, potion, dice = None):
    """
    Drink a potion
    @param model: model to use
    @param character: character drinking a potion
    @param potion: potion to drink
    @param dice: optional prerolled dice
    """
    logger.debug(character.__str__() + ' drinking ' + potion.__str__())

    assert(model != None)
    assert(character != None)
    assert(potion != None)
    assert(potion in character.inventory)

    if potion.maximum_charges_left() < 1:
        logger.warn(character.__str__() +
                    ' tried to drink an empty potion ' +
                    potion.__str__())
        return

    #drinking a potion usually identifies it
    character.identify_item(potion)

    if hasattr(potion, 'effects'):
        for effect in potion.effects['on drink']:
            pyherc.rules.magic.cast_effect(model, character, effect, dice)
            effect.charges = effect.charges - 1

    if potion.maximum_charges_left() < 1:
        character.inventory.remove(potion)

    logger.debug(character.__str__() + ' drank ' + potion.__str__())

