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

@when(u'{attacker_name} hits {target_name}')
def impl(context, attacker_name, target_name):
    attackers = [x for x in context.characters
                 if x.name == attacker_name]
    attacker = attackers[0]
    
    targets = [x for x in context.characters
              if x.name == target_name]
    target = targets[0]

    make(attacker, hit(target))

@then(u'{character_name} should have less hitpoints')
def impl(context, character_name):
    characters = [x for x in context.characters
                  if x.name == character_name]
    character = characters[0]
    
    old_hit_points = character.old_values['hit points']
    new_hit_points = character.hit_points
    
    assert new_hit_points < old_hit_points

@then(u'Attack should deal {damage_type} damage')
def impl(context, damage_type):
    assert False
