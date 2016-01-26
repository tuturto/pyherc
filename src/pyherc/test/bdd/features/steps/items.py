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

# flake8: noqa

from behave import step_matcher
from pyherc.data import is_armour, is_boots
from pyherc.test.bdd.features.helpers import (armour_list, default_context,
                                              get_character, get_item,
                                              get_location, misc_item_list,
                                              weapon_list, boots_list)
from pyherc.test.cutesy import drop, make

step_matcher('re')

@given('(?P<character_name>[A-Za-z]+) has (?P<item_name>[A-Za-z]+)')
@default_context
@weapon_list
@armour_list
@misc_item_list
@boots_list
def impl(context, character_name, item_name):
    if item_name in context.armour_list:
        item = context.armour_list[item_name]()
    elif item_name in context.weapon_list:
        item = context.weapon_list[item_name]()
    elif item_name in context.misc_item_list:
        item = context.misc_item_list[item_name]()
    elif item_name in context.boots_list:
        item = context.boots_list[item_name]()

    context.items.append(item)

    character = get_character(context, character_name)

    character.inventory.append(item)

step_matcher('parse')

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

@then('{item_name} should not be in {location_name}')
def impl(context, item_name, location_name):
    if 'inventory' in location_name:
        (word1, word2, character_name) = location_name.split(' ')
        item = get_item(context, item_name)
        character = get_character(context, character_name)

        assert item not in character.inventory
    else:
        item = get_item(context, item_name)
        room = get_location(context, location_name)

        assert item.level != room

@then('{item_name} should be at same place as {character_name}')
def impl(context, item_name, character_name):
    item = get_item(context, item_name)
    character = get_character(context, character_name)

    assert item.location == character.location

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

@given('{character_name} wears {item_name}')
@default_context
@armour_list
@boots_list
def impl(context, character_name, item_name):
    if item_name in context.armour_list:
        item = context.armour_list[item_name]()
    elif item_name in context.boots_list:
        item = context.boots_list[item_name]()

    context.items.append(item)

    character = get_character(context, character_name)
    character.inventory.append(item)

    if is_armour(item):
        character.inventory.armour = item
    elif is_boots(item):
        character.inventory.boots = item
