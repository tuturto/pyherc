# -*- coding: utf-8 -*-

# Copyright (c) 2010-2017 Tuukka Turto
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

from hamcrest import assert_that, greater_than, is_not, less_than, is_
from pyherc.ai.pathfinding import a_star
from pyherc.data.constants import Direction, Duration
from pyherc.data import blocks_movement
from pyherc.data.effects import DamageModifier
from pyherc.data.geometry import find_direction, area_4_around
from pyherc.test.bdd.features.helpers import (default_context, get_character,
                                              get_item, get_location, observed,
                                              with_action_factory)
from pyherc.test.cutesy import Adventurer, Goblin, take_random_step, Wizard, make
from pyherc.test.matchers import is_dead
import pyherc


def whole_level(level, location):
    """a* helper to find all non-blocking tiles around given tile"""
    for tile in area_4_around(location):
        if not blocks_movement(level, tile):
            yield tile

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

    path, connections, updated = a_star(whole_level,
                                        character.location, #TODO: adjacent nodes as first param
                                        place.location,
                                        character.level)
    assert len(path) > 1

    for tile in path[1:]:
        direction = find_direction(character.location,
                                   tile)
        pyherc.vtable['\ufdd0:move'](character,
                                     direction)

@when('{character_name} enters {portal_name}')
@with_action_factory
def impl(context, character_name, portal_name):
    character = get_character(context, character_name)

    pyherc.vtable['\ufdd0:move'](character, Direction.enter)

@when('{character_name} takes a step')
@with_action_factory
def impl(context, character_name):
    character = get_character(context, character_name)
    make(character, take_random_step())

@then('{character_name} should move {delta} than without {armour_name}')
@with_action_factory
def impl(context, character_name, delta, armour_name):
    character = get_character(context, character_name)
    armour = get_item(context, armour_name)

    if delta == 'slower':
        assert_that(character.tick,
                    is_(greater_than(character.speed * Duration.fast)))
    elif delta == 'faster':
        assert_that(character.tick,
                    is_(less_than(character.speed * Duration.fast)))
    else:
        assert False


@then('{character_name} should attack slower than without {weapon_name}')
@with_action_factory
def impl(context, character_name, weapon_name):
    character = get_character(context, character_name)
    weapon = get_item(context, weapon_name)

    assert_that(character.tick,
                is_(greater_than(character.speed * Duration.normal)))
