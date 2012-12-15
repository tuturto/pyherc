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

from pyherc.test.cutesy import Dagger, Sword, Club, LeatherArmour
from pyherc.test.cutesy import make, drop
from pyherc.test.bdd.features.helpers import default_context
from pyherc.test.bdd.features.helpers import get_character, get_item
from pyherc.test.bdd.features.helpers import get_location

@given(u'{character_name} has dagger')
@default_context
def impl(context, character_name):
    dagger = Dagger()
    context.items.append(dagger)

    character = get_character(context, character_name)

    character.inventory.append(dagger)

@given(u'{character_name} has sword')
@default_context
def impl(context, character_name):
    sword = Sword()
    context.items.append(sword)

    character = get_character(context, character_name)

    character.inventory.append(sword)

@when(u'{character_name} drops {item_name}')
def impl(context, character_name, item_name):
    character = get_character(context, character_name)
    item = get_item(context, item_name)

    make(character, drop(item))

@then(u'{item_name} should be in {location_name}')
def impl(context, item_name, location_name):
    item = get_item(context, item_name)
    room = get_location(context, location_name)

    assert item.level == room

@then(u'{item_name} should be at same place as {character_name}')
def impl(context, item_name, character_name):
    item = get_item(context, item_name)
    character = get_character(context, character_name)

    assert item.location == character.location

@then(u'{item_name} should not be in inventory of {character_name}')
def impl(context, item_name, character_name):
    item = get_item(context, item_name)
    character = get_character(context, character_name)

    assert not item in character.inventory

@given(u'{character_name} wields dagger')
@default_context
def impl(context, character_name):
    dagger = Dagger()
    context.items.append(dagger)

    character = get_character(context, character_name)

    character.inventory.append(dagger)
    character.inventory.weapon = dagger

@given(u'{character_name} wields sword')
@default_context
def impl(context, character_name):
    sword = Sword()
    context.items.append(sword)

    character = get_character(context, character_name)

    character.inventory.append(sword)
    character.inventory.weapon = sword

@given(u'{character_name} wields club')
@default_context
def impl(context, character_name):
    club = Club()
    context.items.append(club)

    character = get_character(context, character_name)

    character.inventory.append(club)
    character.inventory.weapon = club

@given(u'{character_name} wears {armour_name}')
@default_context
def impl(context, character_name, armour_name):
    armour = LeatherArmour()
    context.items.append(armour)

    character = get_character(context, character_name)
    character.inventory.append(armour)
    character.inventory.armour = armour
