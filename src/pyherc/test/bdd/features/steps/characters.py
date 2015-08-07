# -*- coding: utf-8 -*-

#   Copyright 2010-2015 Tuukka Turto
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

# flake8: noqa

from hamcrest import assert_that, greater_than, is_not
from pyherc.ai.pathfinding import a_star
from pyherc.data.constants import Direction, Duration
from pyherc.data.effects import DamageModifier
from pyherc.data.geometry import find_direction
from pyherc.test.bdd.features.helpers import (default_context, get_character,
                                              get_item, get_location, observed,
                                              with_action_factory)
from pyherc.test.cutesy import Adventurer, Goblin, take_random_step, Wizard
from pyherc.test.matchers import is_dead


@given('{character_name} is Adventurer')
@observed
@default_context
def impl(context, character_name):
    new_character = Adventurer()
    new_character.name = character_name
    new_character.model = context.model
    context.characters.append(new_character)

@given('{character_name} is Wizard')
@observed
@default_context
def impl(context, character_name):
    new_character = Wizard()
    new_character.name = character_name
    new_character.model = context.model
    context.characters.append(new_character)

@given('{character_name} is Goblin')
@observed
@default_context
def impl(context, character_name):
    new_character = Goblin()
    new_character.name = character_name
    new_character.model = context.model
    context.characters.append(new_character)

@then('{character_name} should be dead')
def impl(context, character_name):
    character = get_character(context, character_name)
    assert_that(character, is_dead())

@then('{character_name} should be alive')
def step_impl(context, character_name):
    character = get_character(context, character_name)
    assert_that(character, is_not(is_dead()))

@given('{character_name} is almost dead')
@observed
def impl(context, character_name):
    character = get_character(context, character_name)

    character.hit_points = 1

@given('{character_name} is suspectible against {damage_type}')
def impl(context, character_name, damage_type):
    character = get_character(context, character_name)

    modifier = DamageModifier(modifier=2,
                              damage_type=damage_type,
                              duration=None,
                              frequency=None,
                              tick=None,
                              icon=101,
                              title='weak against {0}'.format(damage_type),
                              description='{0} causes extra damage'.format(damage_type))
    character.add_effect(modifier)

@given('{character_name} is Player')
def impl(context, character_name):
    character = get_character(context, character_name)

    model = context.model
    model.player = character

@when('{character_name} walks on {location_name}')
@with_action_factory
def impl(context, character_name, location_name):
    character = get_character(context, character_name)
    place = get_location(context, location_name)

    path, connections, updated = a_star(character.location,
                                        place.location,
                                        character.level)
    assert len(path) > 1

    for tile in path[1:]:
        direction = find_direction(character.location,
                                   tile)
        context.actions_port.move_character(character,
                                            direction)

@when('{character_name} enters {portal_name}')
@with_action_factory
def impl(context, character_name, portal_name):
    character = get_character(context, character_name)

    context.actions_port.move_character(character, Direction.enter)

@when('{character_name} takes a step')
@with_action_factory
def impl(context, character_name):
    character = get_character(context, character_name)
    make(character, take_random_step())

@then('{character_name} should move slower than without {armour_name}')
@with_action_factory
def impl(context, character_name, armour_name):
    character = get_character(context, character_name)
    armour = get_item(context, armour_name)

    assert_that(character.tick,
                is_(greater_than(character.speed * Duration.fast)))

@then('{character_name} should attack slower than without {weapon_name}')
@with_action_factory
def impl(context, character_name, weapon_name):
    character = get_character(context, character_name)
    weapon = get_item(context, weapon_name)

    assert_that(character.tick,
                is_(greater_than(character.speed * Duration.normal)))
