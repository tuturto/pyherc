#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
from pyherc.test.cutesy import make, cast_spell

@when('{caster_name} casts {spell_and_target}')
def impl(context, caster_name, spell_and_target):
    # Simon casts magic missile on Uglak
    # Simon casts healing wind
    caster = get_character(context, caster_name)
    spell = spell_and_target

    make(caster, cast_spell(spell_name = spell))

