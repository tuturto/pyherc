# -*- coding: utf-8 -*-

#   Copyright 2010-2015 Tuukka Turto
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

from hamcrest import assert_that, equal_to, is_, less_than
from pyherc.events import (e_event_type, e_target, e_attacker, e_old_hit_points,
                           e_new_hit_points, e_damage)
from pyherc.test.bdd.features.helpers import get_character
from pyherc.test.cutesy import hit, make
from pyherc.test.cutesy.dictionary import add_history_value, get_history_value


@when('{attacker_name} hits {target_name}')
def impl(context, attacker_name, target_name):
    attacker = get_character(context, attacker_name)
    target = get_character(context, target_name)

    make(attacker, hit(target))

@then('{character_name} should have less hitpoints')
def impl(context, character_name):
    character = get_character(context, character_name)

    old_hit_points = get_history_value(character, 'hit_points')
    new_hit_points = character.hit_points

    assert new_hit_points < old_hit_points

@then('Attack should deal {damage_type} damage')
def impl(context, damage_type):
    observer = context.observer

    attack_hit_events = (x for x in context.observer.events
                         if e_event_type(x) == 'attack hit')

    found = False
    for event in attack_hit_events:
        damage_list = e_damage(event)[1]
        for damage in damage_list:
            if damage_type == damage[1]:
                found = True

    assert found

@then('{character_name} should suffer extra damage')
def impl(context, character_name):
    character = get_character(context, character_name)

    old_hit_points = get_history_value(character, 'hit_points')
    new_hit_points = character.hit_points
    total_damage_suffered = old_hit_points - new_hit_points

    attack_hit_events = (x for x in context.observer.events
                         if e_event_type(x) == 'attack hit')
    matching_events = [x for x in attack_hit_events
                       if e_target(x).name == character_name]
    hit_event = matching_events[0]
    attacker = e_attacker(hit_event)

    total_damage_from_weapon = sum([x[0] for x
                                   in attacker.inventory.weapon.weapon_data.damage])

    assert(total_damage_suffered > total_damage_from_weapon)

@then('damage should be reduced')
def impl(context):
    observer = context.observer

    hp_events = [x for x in observer.events
                 if e_event_type(x) == 'hit points changed']

    hp_event = hp_events[0]

    attack_events = [x for x in observer.events
                     if e_event_type(x) == 'attack hit']

    if attack_events:
        attack_event = attack_events[0]

        weapon = e_attacker(attack_event).inventory.weapon

        expected_damage = sum(x[0] for x in weapon.weapon_data.damage)
        realised_damage = e_old_hit_points(hp_event) - e_new_hit_points(hp_event)

    else:
        trap_event = [x for x in observer.events
                      if e_event_type(x) == 'damage trap triggered'][0]
        expected_damage = 2
        realised_damage = e_damage(trap_event)[0]

    assert_that(realised_damage, is_(less_than(expected_damage)))

@then('damage should be {damage_amount}')
def impl(context, damage_amount):
    observer = context.observer
    damage = int(damage_amount)

    hp_events = [x for x in observer.events
                 if e_event_type(x) == 'hit points changed']
    hp_event = hp_events[0]

    realised_damage = e_old_hit_points(hp_event) - e_new_hit_points(hp_event)

    assert_that(realised_damage, is_(equal_to(damage)))

@then('{character_name} should be in full health')
def impl(context, character_name):
    character = get_character(context, character_name)

    assert_that(character.hit_points, equal_to(character.max_hp))
