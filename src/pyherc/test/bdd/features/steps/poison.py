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

from pyherc.test.bdd.features.helpers import get_character
from pyherc.test.cutesy import affect, potent_poison, weak_poison


@when('{character_name} suffers from {effect_name}')
def impl(context, character_name, effect_name):

    if effect_name == 'weak poison':
        poison_spec = weak_poison()
    elif effect_name == 'strong poison':
        poison_spec = potent_poison()

    character = get_character(context, character_name)

    affect(character, poison_spec)
