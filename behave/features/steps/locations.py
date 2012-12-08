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
from hamcrest import assert_that, is_in, is_not

@given(u'{character_name} is standing in {location_name}')
def impl(context, character_name, location_name):
    context.places = []
    room = Level()
    room.name = location_name
    context.places.append(room)
    
    characters = [x for x in context.characters
                  if x.name == character_name]
    character = characters[0]
    
    place(character, middle_of(room))

@given(u'{character_name} is standing next to {target_name}')
def impl(context, character_name, target_name):
    characters = [x for x in context.characters
                  if x.name == character_name]
    character = characters[0]
    
    characters = [x for x in context.characters
                  if x.name == target_name]
    target = characters[0]
    
    level = target.level
    location = (target.location[0] + 1, 
                target.location[1])

    level.add_creature(character, location)

@given(u'{location_name} is away from {character_name}')
def impl(context, location_name, character_name):
    places = [x for x in context.places
              if x.name == location_name]
    place = places[0]
    
    characters = [x for x in context.characters
                  if x.name == character_name]
    character = characters[0]

    if character.location != (2, 2):
        place.location = (2, 2)
    else:
        place.location = (5, 5)
    
@then(u'{character_name} is not in {place_name}')
def impl(context, character_name, place_name):
    characters = [x for x in context.characters
                  if x.name == character_name]
    character = characters[0]

    places = [x for x in context.places
              if x.name == place_name]
    place = places[0]

    assert_that(character, is_not(is_in(place.creatures)))

@given(u'{portal_name} is Portal')
def impl(context, portal_name):
    portal = Portal(icons = [100, 101], 
                    level_generator_name = 'empty')
    portal.name = portal_name
    
    context.places.append(portal)

@given(u'{portal_name} leads outside')
def impl(context, portal_name):
    places = [x for x in context.places
              if x.name == portal_name]
    portal = places[0]
    
    portal.exits_dungeon = True

@then(u'{entity1_name} and {entity2_name} are located at the same place')
def impl(context, entity1_name, entity2_name):
    characters = [x for x in context.characters
                  if x.name == entity1_name]
    character = characters[0]
    
    locations = [x for x in context.places
                 if x.name == entity2_name]
    place = locations[0]
    
    assert character.location == place.location
