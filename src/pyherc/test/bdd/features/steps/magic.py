# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
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

from behave import step_matcher
from pyherc.test.bdd.features.helpers import get_character, get_item
from pyherc.test.cutesy import cast_spell, gain_domain_, make


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
        target = get_character(context=context,
                               character_name=target_name)
    else:
        target = None

    make(caster, cast_spell(spell_name=spell,
                            target=target))

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

    make(caster, gain_domain_(item=item,
                              domain=domain_name))

@then('{caster_name} should have more {domain_name} spells')
def step_impl(context, caster_name, domain_name):
    assert False
