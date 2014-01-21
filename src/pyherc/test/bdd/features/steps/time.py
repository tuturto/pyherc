# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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

from pyherc.test.bdd.features.helpers import get_character
from pyherc.test.cutesy import make, wait_
from pyherc.test.cutesy.dictionary import get_history_value

@then('time should pass for {character_name}')
def impl(context, character_name):
    character = get_character(context, character_name)

    old_time = get_history_value(character, 'tick')
    new_time = character.tick

    assert new_time > old_time

@when('{character_name} waits')
def step_impl(context, character_name):
    character = get_character(context, character_name)

    make(character, wait_())
