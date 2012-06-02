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

"""
Dictionary for behaviour driven tests
"""
from pyherc.test.builders import CharacterBuilder
from pyherc.test.builders import ActionFactoryBuilder
from pyherc.test.builders import LevelBuilder

from pyherc.rules import AttackParameters

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest import assert_that, is_, equal_to
from mockito import mock, when

def strong(character):
    character.body = 10
    return character

def weak(character):
    character.body = 2
    return character

def Adventurer():
    character = (CharacterBuilder()
                    .with_action_factory(ActionFactoryBuilder()
                                            .with_move_factory()
                                            .with_attack_factory()
                                            .with_drink_factory()
                                            .with_inventory_factory())
                    .with_hit_points(10)
                    .with_max_hp(10)
                    .with_speed(5)
                    .with_body(5)
                    .with_mind(5)
                    .with_attack(1)
                    .with_name('Adventurer')
                    .build()
                    )
    return character

def Goblin():
    character = (CharacterBuilder()
                    .with_action_factory(ActionFactoryBuilder()
                                            .with_move_factory()
                                            .with_attack_factory()
                                            .with_drink_factory()
                                            .with_inventory_factory())
                    .with_hit_points(5)
                    .with_max_hp(5)
                    .with_speed(3)
                    .with_body(3)
                    .with_attack(1)
                    .with_name('Goblin')
                    .build()
                    )
    return character

def Level():
    level = (LevelBuilder()
                    .build())
    return level

class LevelLocation(object):
    def __init__(self, level, location):
        super(LevelLocation, self).__init__()
        self.level = level
        self.location = location

    def __str__(self):
        return 'level: {0}, location: {1}'.format(self.level,
                                                  self.location)

def place(character, location):
    location.level.add_creature(character, location.location)

def middle_of(level):
    x_loc = level.get_size()[0] // 2
    y_loc = level.get_size()[1] // 2
    location = LevelLocation(level, (x_loc, y_loc))

    return location

def right_of(object):
    x_loc = object.location[0] + 1
    y_loc = object.location[1]
    location = LevelLocation(object.level, (x_loc, y_loc))

    return location

def make(actor, action):
    action(actor)

class Hit(object):
    def __init__(self, target):
        super(Hit, self).__init__()
        self.target = target

    def __call__(self, attacker):
        rng = mock()
        when(rng).randint(1, 6).thenReturn(1)

        self.target.old_values = {}
        self.target.old_values['hit points'] = self.target.hit_points
        #TODO: direction, attack type
        params = AttackParameters(attacker = attacker,
                                  direction = 3,
                                  attack_type = 'unarmed',
                                  random_number_generator = rng)

        attacker.execute_action(params)

def hit(target):
    action = Hit(target)
    return action

class HasLessHitPoints(BaseMatcher):
    def __init__(self):
        super(HasLessHitPoints, self).__init__()
        self.old_hit_points = None

    def _matches(self, item):
        if hasattr(item, 'old_values'):
            self.old_hit_points = item.old_values['hit points']
            if self.old_hit_points > item.hit_points:
                return True
            else:
                return False
        else:
            return False

    def describe_to(self, description):
        description.append(
                    'Character with less than {0} hitpoints'.format(
                                                        self.old_hit_points))

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append(
                        'Character has {0} hit points'.format(
                                                        item.hit_points))

def has_less_hit_points():
    return HasLessHitPoints()
