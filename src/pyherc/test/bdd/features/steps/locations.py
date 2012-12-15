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

from pyherc.test.cutesy import Level, place, middle_of
from pyherc.data import Portal
from pyherc.test.bdd.features.helpers import default_context
from pyherc.test.bdd.features.helpers import get_character, get_location
from pyherc.test.bdd.features.helpers import get_entity
from hamcrest import assert_that, is_in, is_not

@given(u'{character_name} is standing in {location_name}')
@default_context
def impl(context, character_name, location_name):
    room = Level()
    room.name = location_name
    context.places.append(room)

    character = get_character(context, character_name)

    place(character, middle_of(room))

@given(u'{character_name} is standing next to {target_name}')
def impl(context, character_name, target_name):
    character = get_character(context, character_name)
    target = get_character(context, target_name)

    level = target.level
    location = (target.location[0] + 1,
                target.location[1])

    level.add_creature(character, location)

@given(u'{portal_name} is located in corner of {location_name}')
def impl(context, portal_name, location_name):
    place = get_location(context, location_name)
    portal = get_location(context, portal_name)

    place.add_portal(portal, (2, 2), None)

@then(u'{character_name} is not in {place_name}')
def impl(context, character_name, place_name):
    character = get_character(context, character_name)
    place = get_location(context, place_name)

    assert_that(character, is_not(is_in(place.creatures)))

@given(u'{portal_name} is Portal')
@default_context
def impl(context, portal_name):
    portal = Portal(icons = [100, 101],
                    level_generator_name = 'empty')
    portal.name = portal_name

    context.places.append(portal)

@given(u'{portal_name} leads outside')
def impl(context, portal_name):
    portal = get_location(context, portal_name)

    portal.exits_dungeon = True

@then(u'{entity1_name} and {entity2_name} are located at the same place')
def impl(context, entity1_name, entity2_name):
    character = get_entity(context, entity1_name)
    place = get_entity(context, entity2_name)

    assert character.location == place.location
