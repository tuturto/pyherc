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

from behave import step_matcher
from pyherc.test.bdd.features.helpers import get_character, get_item
from pyherc.test.cutesy import make, cast_spell, gain_domain

@when('{caster_name} casts {spell_and_target}')
def impl(context, caster_name, spell_and_target):
    caster = get_character(context, caster_name)
    split_text = spell_and_target.split()

    if 'on' in split_text:
        on_index = split_text.index('on')
        spell = " ".join(split_text[:on_index])
        target_name = " ".join(split_text[on_index + 1:])
    else:
        spell = spell_and_target
        target_name = None

    if target_name:
        target = get_character(context = context,
                               character_name = target_name)
    else:
        target = None

    make(caster, cast_spell(spell_name = spell,
                            target = target))

step_matcher('re')

@given('^(?P<caster_name>[A-Za-z]+) has no spirit left$')
def impl(context, caster_name):
    caster = get_character(context, caster_name)
    caster.spirit = 0

step_matcher('parse')

@when('{caster_name} uses {item_name} for {domain_name} domain')
def step_impl(context, caster_name, item_name, domain_name):
    caster = get_character(context, caster_name)
    item = get_item(context, item_name)

    make(caster, gain_domain(item = item,
                             domain = domain_name))

@then('{caster_name} should have more {domain_name} spells')
def step_impl(context, caster_name, domain_name):
    assert False
