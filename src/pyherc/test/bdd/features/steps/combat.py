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

from pyherc.test.cutesy import make, hit
from pyherc.test.bdd.features.helpers import get_character
from hamcrest import assert_that, is_, smaller_than

@when(u'{attacker_name} hits {target_name}')
def impl(context, attacker_name, target_name):
    attacker = get_character(context, attacker_name)
    target = get_character(context, target_name)

    make(attacker, hit(target))

@then(u'{character_name} should have less hitpoints')
def impl(context, character_name):
    character = get_character(context, character_name)

    old_hit_points = character.old_values['hit points']
    new_hit_points = character.hit_points

    assert new_hit_points < old_hit_points

@then(u'Attack should deal {damage_type} damage')
def impl(context, damage_type):
    observer = context.observer

    attack_hit_events = (x for x in context.observer.events
                         if x.event_type == 'attack hit')

    matching_events = [x for x in attack_hit_events
                       if damage_type in x.damage.damage_types]

    assert len(matching_events) > 0

@then(u'{character_name} should suffer extra damage')
def impl(context, character_name):
    character = get_character(context, character_name)

    old_hit_points = character.old_values['hit points']
    new_hit_points = character.hit_points
    total_damage_suffered = old_hit_points - new_hit_points

    attack_hit_events = (x for x in context.observer.events
                         if x.event_type == 'attack hit')
    matching_events = [x for x in attack_hit_events
                       if x.target.name == character_name]
    hit_event = matching_events[0]
    attacker = hit_event.attacker

    total_damage_from_weapon = sum([x[0] for x in attacker.inventory.weapon.weapon_data.damage])

    assert(total_damage_suffered > total_damage_from_weapon)

@then(u'Attack damage should be reduced')
def impl(context):
    observer = context.observer

    hp_events = [x for x in observer.events
                 if hasattr(x, 'old_hit_points')
                 and hasattr(x, 'new_hit_points')]

    hp_event = hp_events[0]

    attack_events = [x for x in observer.events
                     if hasattr(x, 'attacker')
                     and hasattr(x, 'target')]

    attack_event = attack_events[0]

    weapon = attack_event.attacker.inventory.weapon

    expected_damage = sum(x[0] for x in weapon.weapon_data.damage)
    realised_damage = hp_event.old_hit_points - hp_event.new_hit_points

    assert_that(realised_damage, is_(smaller_than(expected_damage)))
