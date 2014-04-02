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

# flake8: noqa

from hamcrest import assert_that, has_length
from pyherc.test.bdd.features.helpers import get_character


@then('{character_name} should be on fire')
def step_impl(context, character_name):
    character = get_character(context, character_name)

    effects = [effect for effect in character.get_effects()
               if effect.damage_type == 'fire']

    assert_that(effects, has_length(1))
