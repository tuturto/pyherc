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
from pyherc.test.builders import ItemBuilder

from pyherc.rules import AttackParameters
from pyherc.data.effects import Poison

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest import assert_that, is_, equal_to
from mockito import mock, when

def strong(character):
    """
    Modifies character to be strong

    :param character: character to modify
    :type character: Character
    """
    character.body = 10
    character.hit_points = 20
    character.maximum_hit_points = 20
    return character

def weak(character):
    """
    Modifies character to be weak

    :param character: character to modify
    :type character: Character
    """
    character.body = 2
    character.hit_points = 5
    character.maximum_hit_points = 5
    return character

def Adventurer():
    """
    Creates a adventurer character

    :returns: fully initialised adventurer
    :rtype: Character
    """
    character = (CharacterBuilder()
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

def Goblin(action = None):
    """
    Creates a goblin

    :returns: fully initialised goblin
    :rtype: Character
    """
    character = (CharacterBuilder()
                    .with_hit_points(5)
                    .with_max_hp(5)
                    .with_speed(3)
                    .with_body(3)
                    .with_attack(1)
                    .with_name('Goblin')
                    .build()
                    )
    if action != None:
        action(character)

    return character

def Dagger():
    """
    Creates a dagger
    """
    item = (ItemBuilder()
                .with_name('dagger')
                .with_damage(2)
                .build())

    return item

def Level():
    """
    Creates a level

    :returns: fully initialised level
    :rtype: Level
    """
    level = (LevelBuilder()
                    .build())
    return level

class LevelLocation(object):
    """
    Defines a location in game world
    """
    def __init__(self, level, location):
        """
        Default constructor

        :param level: level where location is
        :type level: Level
        :param location: location within level
        :type location: (int, int)
        """
        super(LevelLocation, self).__init__()
        self.level = level
        self.location = location

    def __str__(self):
        """
        Create string representation of location
        """
        return 'level: {0}, location: {1}'.format(self.level,
                                                  self.location)

def place(character, location):
    """
    Place character to given location

    :param character: character to place
    :type character: Character
    :param location: location to place the character
    :type location: LevelLocation
    """
    location.level.add_creature(character, location.location)

def middle_of(level):
    """
    Find out middle point of level

    :param level: level to inspect
    :type level: Level
    :returns: middle point of level
    :rtype: (int, int)
    """
    x_loc = level.get_size()[0] // 2
    y_loc = level.get_size()[1] // 2
    location = LevelLocation(level, (x_loc, y_loc))

    return location

def right_of(object):
    """
    Find location on the right side of something

    :param object: entity on map
    :type object: Item or Creature
    :returns: point right of the entity
    :rtype: (int, int)
    """
    x_loc = object.location[0] + 1
    y_loc = object.location[1]
    location = LevelLocation(object.level, (x_loc, y_loc))

    return location

def make(actor, action):
    """
    Trigger an action

    :param actor: actor doing the action
    :type actor: Character
    :param action: action to perfrom
    """
    action(actor)

class Hit(object):
    """
    Class representing a hit in unarmed combat
    """
    def __init__(self, target):
        """
        Default constructor

        :param target: target to attack
        """
        super(Hit, self).__init__()
        self.target = target

    def __call__(self, attacker):
        """
        Performs the hit

        :param attacker: character attacking
        :type attacker: Character
        """
        rng = mock()
        when(rng).randint(1, 6).thenReturn(1)

        self.target.old_values = {}
        self.target.old_values['hit points'] = self.target.hit_points

        if len(attacker.weapons) > 0:
            attack_type = 'melee'
        else:
            attack_type = 'unarmed'

        action_factory = (ActionFactoryBuilder()
                                    .with_move_factory()
                                    .with_attack_factory()
                                    .with_drink_factory()
                                    .with_inventory_factory()
                                    .build())

        params = AttackParameters(attacker = attacker,
                                  direction = self.find_direction(attacker.location,
                                                                  self.target.location),
                                  attack_type = attack_type,
                                  random_number_generator = rng)

        attacker.execute_action(params,
                                action_factory)

    def find_direction(self, start, end):
        """
        Find direction from one point to another

        :param start: start location
        :type start: (int, int)
        :param end: end location
        :type end: (int, int)
        """
        direction = 0
        if start[0] > end[0]:
            #to left
            if start[1] < end[1]:
                direction = 8
            elif start[1] > end[1]:
                direction = 6
            else:
                direction = 7
        elif start[0] < end[0]:
            #to right
            if start[1] < end[1]:
                direction = 2
            elif start[1] > end[1]:
                direction = 4
            else:
                direction = 3
        elif start[1] < end[1]:
            #down
            direction = 5
        else:
            #up
            direction = 1
        return direction


def hit(target):
    """
    Hit target

    :param target: target to hit
    :returns: callable action
    """
    action = Hit(target)
    return action

class WieldAction(object):
    """
    Action to get chracter to wield something
    """
    def __init__(self, weapon):
        """
        Default constructor

        :param weapon: weapon to wield
        :type weapon: Item
        """
        self.weapon = weapon

    def __call__(self, character):
        """
        Wield the item

        :param character: character wielding the weapon
        :type character: Character
        """
        character.weapons.append(self.weapon)
        return character

def wielding(weapon):
    """
    Make a character to wield a weapon
    """
    action = WieldAction(weapon)
    return action

class HasLessHitPoints(BaseMatcher):
    """
    Matcher for checking that hit points have gone down
    """
    def __init__(self):
        """
        Default constructor
        """
        super(HasLessHitPoints, self).__init__()
        self.old_hit_points = None

    def _matches(self, item):
        """
        Check if match

        :param item: match against this item
        """
        if hasattr(item, 'old_values'):
            self.old_hit_points = item.old_values['hit points']
            if self.old_hit_points > item.hit_points:
                return True
            else:
                return False
        else:
            return False

    def describe_to(self, description):
        """
        Descripe the match

        :param description: description text to append
        :type description: string
        """
        description.append(
                    'Character with less than {0} hitpoints'.format(
                                                        self.old_hit_points))

    def describe_mismatch(self, item, mismatch_description):
        """
        Descripe the mismatch

        :item: mismatching item
        :param mismatch_description: description text to append
        :type mismatch_description: string
        """
        mismatch_description.append(
                        'Character has {0} hit points'.format(
                                                        item.hit_points))

def has_less_hit_points():
    """
    Check that hit points have gone down
    """
    return HasLessHitPoints()

def at_(loc_x, loc_y):
    """
    Create a new location entity

    :param loc_x: x-coordinate of location
    :type loc_x: int
    :param loc_y: y-coordinate of location
    :type loc_y: int
    :returns: location
    :rtype: (int, int)
    """
    return (loc_x, loc_y)

def affect(target, effect_spec):
    """
    Triggers an effect on target

    :param target: target of the effect
    :type target: Character
    :param effect_spec: effect specification
    :type effect_spec: {}
    """
    effect_type = effect_spec['effect_type']
    del effect_spec['effect_type']
    effect_spec['target'] = target

    new_effect = effect_type(**effect_spec)

    new_effect.trigger()

def with_(effect_spec):
    """
    Syntactic sugar

    :param effect_spec: effect specification
    :type effect_spec: {}
    :returns: effect specification
    :rtype: {}
    """
    return effect_spec

def potent_poison(target = None):
    """
    Creates effect specification for poison

    :param target: target of the effect
    :type target: Character
    :returns: effect specification
    :rtype: {}
    """
    return {'effect_type': Poison,
            'duration': 1,
            'frequency': 1,
            'tick': 0,
            'damage': 100,
            'target': target}
