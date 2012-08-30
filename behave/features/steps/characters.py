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

from pyherc.test.cutesy import Adventurer, Goblin
from pyherc.test.matchers import is_dead, is_not_in
from hamcrest import assert_that

@given(u'{character_name} is Adventurer')
def impl(context, character_name):
    if not hasattr(context, 'characters'):
        context.characters = []
    new_character = Adventurer()
    new_character.name = character_name
    context.characters.append(new_character)

@given(u'{character_name} is Goblin')
def impl(context, character_name):
    if not hasattr(context, 'characters'):
        context.characters = []
    new_character = Goblin()
    new_character.name = character_name
    context.characters.append(new_character)

@then(u'{character_name} should be dead')
def impl(context, character_name):
    characters = [x for x in context.characters
                  if x.name == character_name]
    character = characters[0]

    assert_that(character, is_dead())

@given(u'{character_name} is almost dead')
def impl(context, character_name):
    characters = [x for x in context.characters
                  if x.name == character_name]
    character = characters[0]
    
    character.hit_points = 1
