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

from hamcrest import assert_that, is_in, is_not
from pyherc.data import Portal, add_portal, add_character, remove_character
from pyherc.test.bdd.features.helpers import (default_context, get_character,
                                              get_entity, get_location)
from pyherc.test.cutesy import Level, middle_of, place


@given('{character_name} is standing in {location_name}')
@default_context
def impl(context, character_name, location_name):
    room = Level()
    room['name'] = location_name
    context.places.append(room)

    character = get_character(context, character_name)

    place(character, middle_of(room))

@given('{character_name} is standing next to {target_name}')
def impl(context, character_name, target_name):
    character = get_character(context, character_name)
    target = get_character(context, target_name)

    if not target.level:
        room = Level()
        room['name'] = 'room'
        context.places.append(room)
        place(target, middle_of(room))

    level = target.level

    location = (target.location[0] + 1,
                target.location[1])

    remove_character(level, character)
    add_character(level, location, character)

@given('{character_name} is standing away from {target_name}')
def impl(context, character_name, target_name):
    character = get_character(context, character_name)
    target = get_character(context, target_name)

    if not target.level:
        room = Level()
        room['name'] = 'room'
        context.places.append(room)
        place(target, middle_of(room))

    level = target.level
    location = (target.location[0] + 3,
                target.location[1])

    remove_character(level, character)
    add_character(level, location, character)

@given('{portal_name} is located in corner of {location_name}')
def impl(context, portal_name, location_name):
    place = get_location(context, location_name)
    portal = get_location(context, portal_name)

    add_portal(place, (2, 2), portal, None)

@then('{character_name} is not in {place_name}')
def impl(context, character_name, place_name):
    character = get_character(context, character_name)
    place = get_location(context, place_name)

    assert_that(character, is_not(is_in(place['\ufdd0:characters'])))

@given('{portal_name} is Portal')
@default_context
def impl(context, portal_name):
    portal = Portal(icons=[100, 101],
                    level_generator_name='empty')
    portal.name = portal_name

    context.places.append(portal)

@given('{portal_name} leads outside')
def impl(context, portal_name):
    portal = get_location(context, portal_name)

    portal.exits_dungeon = True

@then('{entity1_name} and {entity2_name} are located at the same place')
def impl(context, entity1_name, entity2_name):
    character = get_entity(context, entity1_name)
    place = get_entity(context, entity2_name)

    assert character.location == place.location
