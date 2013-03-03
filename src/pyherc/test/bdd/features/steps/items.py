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

from pyherc.test.cutesy import make, drop
from pyherc.test.bdd.features.helpers import default_context, armour_list
from pyherc.test.bdd.features.helpers import weapon_list
from pyherc.test.bdd.features.helpers import get_character, get_item
from pyherc.test.bdd.features.helpers import get_location

@given('{character_name} has {item_name}')
@default_context
@weapon_list
@armour_list
def impl(context, character_name, item_name):
    if item_name in context.armour_list:
        item = context.armour_list[item_name]()
    elif item_name in context.weapon_list:
        item = context.weapon_list[item_name]()

    context.items.append(item)

    character = get_character(context, character_name)

    character.inventory.append(item)

@when('{character_name} drops {item_name}')
def impl(context, character_name, item_name):
    character = get_character(context, character_name)
    item = get_item(context, item_name)

    make(character, drop(item))

@then('{item_name} should be in {location_name}')
def impl(context, item_name, location_name):
    if 'inventory' in location_name:
        (word1, word2, character_name) = location_name.split(' ')
        item = get_item(context, item_name)
        character = get_character(context, character_name)

        assert item in character.inventory
    else:
        item = get_item(context, item_name)
        room = get_location(context, location_name)

        assert item.level == room

@then('{item_name} should be at same place as {character_name}')
def impl(context, item_name, character_name):
    item = get_item(context, item_name)
    character = get_character(context, character_name)

    assert item.location == character.location

@then('{item_name} should not be in inventory of {character_name}')
def impl(context, item_name, character_name):
    item = get_item(context, item_name)
    character = get_character(context, character_name)

    assert not item in character.inventory

@given('{character_name} wields {weapon_name}')
@default_context
@weapon_list
def impl(context, character_name, weapon_name):

    character = get_character(context, character_name)

    if 'and' in weapon_name:
        weapons = weapon_name.split(' and ')
        weapon = context.weapon_list[weapons[0]]()
        ammunition = context.weapon_list[weapons[1]]()

        character.inventory.append(ammunition)
        character.inventory.projectiles = ammunition
    else:
        weapon = context.weapon_list[weapon_name]()

    context.items.append(weapon)
    character.inventory.append(weapon)
    character.inventory.weapon = weapon

@given('{character_name} wears {armour_name}')
@default_context
@armour_list
def impl(context, character_name, armour_name):
    armour = context.armour_list[armour_name]()
    context.items.append(armour)

    character = get_character(context, character_name)
    character.inventory.append(armour)
    character.inventory.armour = armour
