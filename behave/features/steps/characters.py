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

from pyherc.data.effects import DamageModifier
from pyherc.test.cutesy import Adventurer, Goblin
from pyherc.test.matchers import is_dead, is_not_in
from pyherc.test.helpers import observed, with_action_factory
from pyherc.ai.pathfinding import a_star
from hamcrest import assert_that

@given(u'{character_name} is Adventurer')
@observed
def impl(context, character_name):
    if not hasattr(context, 'characters'):
        context.characters = []
    new_character = Adventurer()
    new_character.name = character_name
    new_character.model = context.model
    context.characters.append(new_character)

@given(u'{character_name} is Goblin')
@observed
def impl(context, character_name):
    if not hasattr(context, 'characters'):
        context.characters = []
    new_character = Goblin()
    new_character.name = character_name
    new_character.model = context.model
    context.characters.append(new_character)

@then(u'{character_name} should be dead')
def impl(context, character_name):
    characters = [x for x in context.characters
                  if x.name == character_name]
    character = characters[0]

    assert_that(character, is_dead())

@given(u'{character_name} is almost dead')
@observed
def impl(context, character_name):
    characters = [x for x in context.characters
                  if x.name == character_name]
    character = characters[0]
    
    character.hit_points = 1

@given(u'{character_name} is suspectible against {damage_type}')
def impl(context, character_name, damage_type):
    characters = [x for x in context.characters
                  if x.name == character_name]
    character = characters[0]

    modifier = DamageModifier(modifier = 2,
                              damage_type = damage_type,
                              duration = None,
                              frequency = None,
                              tick = None,
                              icon = 101,
                              title = 'weak against {0}'.format(damage_type),
                              description = '{0} causes extra damage'.format(damage_type))
    character.add_effect(modifier)

@given(u'{character_name} is Player')
def impl(context, character_name):
    characters = [x for x in context.characters
                  if x.name == character_name]
    character = characters[0]
    
    model = context.model   
    model.player = character

@when(u'{character_name} walks on {location_name}')
@with_action_factory
def impl(context, character_name, location_name):
    characters = [x for x in context.characters
                  if x.name == character_name]
    character = characters[0]

    places = [x for x in context.places
              if x.name == location_name]
    place = places[0]
    
    path, connections, updated = a_star(character.location,
                                        place.location,
                                        character.level)
    for tile in path[1:]:
        direction = find_direction(character.location,
                                   tile)
        character.move(direction,
                       context.action_factory)

@when(u'{character_name} enters {portal_name}')
@with_action_factory
def impl(context, character_name, portal_name):
    characters = [x for x in context.characters
                  if x.name == character_name]
    character = characters[0]
    
    character.move(9,
                   context.action_factory)
    
def find_direction(start, end):
    direction = None
    if start[0] < end[0]:
        #right side
        if start[1] < end[1]:
            #right, below
            direction = 4
        elif start[1] > end[1]:
            #right, above
            direction = 2
        else:
            #right
            direction = 3
    elif start[0] > end[0]:
        #left side
        if start[1] < end[1]:
            #left, below
            direction = 6
        elif start[1] > end[1]:
            #left, above
            direction = 8
        else:
            #left
            direction = 7
    else:
        #up or down
        if start[1] < end[1]:
            #below
            direction = 5
        elif start[1] > end[1]:
            #above
            direction = 1

    return direction
