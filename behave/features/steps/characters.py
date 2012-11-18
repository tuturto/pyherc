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
from pyherc.test.helpers import Observed
from hamcrest import assert_that

@given(u'{character_name} is Adventurer')
@Observed()
def impl(context, character_name):
    if not hasattr(context, 'characters'):
        context.characters = []
    new_character = Adventurer()
    new_character.name = character_name
    new_character.model = context.model
    context.characters.append(new_character)

@given(u'{character_name} is Goblin')
@Observed()
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
@Observed()
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
