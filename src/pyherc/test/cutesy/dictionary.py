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

"""
Dictionary for behaviour driven tests
"""
from hamcrest.core.base_matcher import BaseMatcher
from mockito import mock, when
from pyherc.generators import get_effect_creator
from pyherc.data.effects import DamageEffect, Heal, Poison
from pyherc.data import level_size, get_items, add_character
from pyherc.data.geometry import find_direction
from pyherc.rules import Dying
from pyherc.ports import (attack, is_move_legal, move, set_action_factory, wait,
                          drop_item, cast, gain_domain)
from pyherc.test.builders import (ActionFactoryBuilder,
                                  LevelBuilder, SpellCastingFactoryBuilder,
                                  SpellGeneratorBuilder)


def add_history_value(character, attribute):
    """
    Add given value into history data of the character

    :param character: Character to modify
    :type character: Character
    :param attribute: name of the attribute to store
    :type attribute: String

    .. versionadded:: 0.10
    """
    if not hasattr(character, 'old_values'):
        character.old_values = {}

    if hasattr(getattr(character, attribute), 'copy'):
        character.old_values[attribute] = getattr(character, attribute).copy()
    else:
        character.old_values[attribute] = getattr(character, attribute)


def get_history_value(character, attribute):
    """
    Get given history value

    :param character: character whose history value to get
    :type character: Character
    :param attribute: name of the attribute
    :type attribute: String
    :returns: old value of the attribute

    .. versionadded:: 0.10
    """
    return character.old_values[attribute]


def Level():
    """
    Creates a level

    :returns: fully initialised level
    :rtype: Level
    """
    level = (LevelBuilder()
             .build())
    return level


class LevelLocation():
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
        super().__init__()
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
    add_character(location.level, location.location, character)


def middle_of(level):
    """
    Find out middle point of level

    :param level: level to inspect
    :type level: Level
    :returns: middle point of level
    :rtype: (int, int)
    """
    size = level_size(level)
    x_loc = size[1] // 2
    y_loc = size[3] // 2
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


class Wait():
    """
    Class representing waiting a bit
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def __call__(self, character):
        """
        Performs waiting

        :param character: character waiting
        :type character: Character
        """
        add_history_value(character, 'tick')

        set_action_factory(ActionFactoryBuilder()
                           .with_wait_factory()
                           .build()) # TODO: mutating global state is bad

        wait(character)


def wait_():
    """
    Wait a bit
    """
    action = Wait()
    return action


class TakeRandomStep():
    """
    Class representing taking a random step
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def __call__(self, character):
        """
        Performs taking a single step

        :param character: character walking
        :type character: Character
        """
        add_history_value(character, 'tick')

        action_factory = (ActionFactoryBuilder()
                          .with_move_factory()
                          .build())

        directions = [direction for direction in range(1, 9)
                      if is_move_legal(character,
                                       direction)]

        assert len(directions) > 0

        move(character=character,
             direction=directions[0])


def take_random_step():
    """
    Take a single step
    """
    return TakeRandomStep()


class CastSpell():
    """
    Class representing casting a spell
    """
    def __init__(self, spell_name, target=None):
        """
        Default constructor

        :param spell_name: name of the spell to cast
        :type spell_name: string
        :param target: target of the spell
        :type target: Character
        """
        super().__init__()
        self.spell_name = spell_name
        self.target = target

    def __call__(self, caster):
        """
        Performs the casting

        :param caster: character doing the casting
        :type caster: Character
        """
        add_history_value(caster, 'hit_points')

        spell_factory = SpellGeneratorBuilder().build()

        effects_factory = get_effect_creator({'heal medium wounds':
                                        {'type': Heal,
                                         'duration': None,
                                         'frequency': None,
                                         'tick': 0,
                                         'healing': 10,
                                         'icon': None,
                                         'title': 'Heal medium wounds',
                                         'description': 'Heals medium amount of damage'},  # noqa
                                    'cause wound':
                                        {'type': DamageEffect,
                                         'duration': None,
                                         'frequency': None,
                                         'tick': 0,
                                         'damage': 5,
                                         'damage_type': 'magic',
                                         'icon': None,
                                         'title': 'Cause minor wound',
                                         'description': 'Causes minor amount of damage'},  # noqa
                                    'fire':
                                        {'type': DamageEffect,
                                         'duration': 30,
                                         'frequency': 5,
                                         'tick': 0,
                                         'damage': 3,
                                         'damage_type': 'fire',
                                         'icon': None,
                                         'title': 'Fire',
                                         'description': 'You are on fire!'}})

        spell_casting_factory = (SpellCastingFactoryBuilder()
                                 .with_spell_factory(spell_factory)
                                 .with_effects_factory(effects_factory)
                                 .build())

        set_action_factory(ActionFactoryBuilder()
                           .with_dying_rules()
                           .with_spellcasting_factory(spell_casting_factory)
                           .build()) # TODO: mutating global state is bad

        if self.target:
            direction = find_direction(caster.location,
                                       self.target.location)
        else:
            direction = 1

        cast(caster,
             direction=direction,
             spell_name=self.spell_name)


def cast_spell(spell_name, target=None):
    """
    Cast a spell

    :param spell_name: name of the spell to cast
    """
    action = CastSpell(spell_name, target)
    return action


class Hit():
    """
    Class representing a hit in unarmed combat
    """
    def __init__(self, target):
        """
        Default constructor

        :param target: target to attack
        """
        super().__init__()
        self.target = target

    def __call__(self, attacker):
        """
        Performs the hit

        :param attacker: character attacking
        :type attacker: Character
        """
        add_history_value(self.target, 'hit_points')

        rng = mock()
        when(rng).randint(1, 6).thenReturn(1)

        action_factory = (ActionFactoryBuilder()
                          .with_move_factory()
                          .with_attack_factory()
                          .with_drink_factory()
                          .with_inventory_factory()
                          .with_dying_rules()
                          .build())

        set_action_factory(action_factory) # TODO: mutating global state is bad
        attack(attacker,
               find_direction(attacker.location,
                              self.target.location),
               rng)


def hit(target):
    """
    Hit target

    :param target: target to hit
    :returns: callable action
    """
    action = Hit(target)
    return action


class WieldAction():
    """
    Action to get chracter to wield something
    """
    def __init__(self, weapon):
        """
        Default constructor

        :param weapon: weapon to wield
        :type weapon: Item
        """
        super().__init__()
        self.weapon = weapon

    def __call__(self, character):
        """
        Wield the item

        :param character: character wielding the weapon
        :type character: Character
        """
        character.inventory.weapon = self.weapon
        return character


def wielding(weapon):
    """
    Make a character to wield a weapon
    """
    action = WieldAction(weapon)
    return action


class GainDomainAction():
    """
    Action to gain a domain
    """

    def __init__(self, item, domain):
        """
        Default constructor
        """
        super().__init__()
        self.item = item
        self.domain = domain

    def __call__(self, character):
        """
        Execute the action
        """
        set_action_factory(ActionFactoryBuilder()
                           .with_gain_domain_factory()
                           .with_dying_rules()
                           .build()) # TODO: mutating global state is bad

        gain_domain(character=character,
                    item=self.item,
                    domain=self.domain)


def gain_domain_(item, domain):
    """
    Gain domain
    """
    return GainDomainAction(item=item,
                            domain=domain)


class HasLessHitPoints(BaseMatcher):
    """
    Matcher for checking that hit points have gone down
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()
        self.old_hit_points = None

    def _matches(self, item):
        """
        Check if match

        :param item: match against this item
        """
        self.old_hit_points = get_history_value(item, 'hit_points')

        if self.old_hit_points > item.hit_points:
            return True
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
            'Character has {0} hit points'.format(item.hit_points))


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

    add_history_value(target, 'hit_points')

    new_effect.trigger(Dying())


def with_(effect_spec):
    """
    Syntactic sugar

    :param effect_spec: effect specification
    :type effect_spec: {}
    :returns: effect specification
    :rtype: {}
    """
    return effect_spec


def potent_poison(target=None):
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
            'target': target,
            'icon': 101,
            'title': 'potent poison',
            'description': 'causes huge amount of damage'}


def weak_poison(target=None):
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
            'damage': 1,
            'target': target,
            'icon': 101,
            'title': 'weak poison',
            'description': 'causes tiny amount of damage'}


class CarryAction():
    """
    Action to get chracter to carry something
    """
    def __init__(self, item):
        """
        Default constructor

        :param item: item to carry
        :type item: Item
        """
        super().__init__()
        self.item = item

    def __call__(self, character):
        """
        Put item in inventory

        :param character: character carrying the item
        :type character: Character
        """
        character.inventory.append(self.item)
        return character


def carrying(item):
    """
    make character to carry an item
    """
    action = CarryAction(item)
    return action


class Drop():
    """
    Class representing dropping an item
    """
    def __init__(self, item):
        """
        Default constructor

        :param item: item to drop
        """
        super().__init__()
        self.item = item

    def __call__(self, actor):
        """
        Performs the drop action

        :param actor: character dropping the item
        :type actor: Character
        """
        add_history_value(actor, 'location')
        add_history_value(actor, 'level')
        add_history_value(actor, 'inventory')
        add_history_value(actor, 'tick')

        set_action_factory(ActionFactoryBuilder()
                           .with_move_factory()
                           .with_attack_factory()
                           .with_drink_factory()
                           .with_inventory_factory()
                           .build()) # TODO: mutating global state is bad

        drop_item(actor,
                  self.item)


def drop(item):
    """
    make chracter to drop an item
    """
    action = Drop(item)
    return action


class HasDropped(BaseMatcher):
    """
    Matcher for checking that item has been dropped
    """
    def __init__(self, item):
        """
        Default constructor
        """
        super().__init__()
        self.item = item
        self.fail_reason = ''

    def _matches(self, item):
        """
        Check if match

        :param item: match against this item
        """
        if self.item in item.inventory:
            self.fail_reason = 'item not dropped'
            return False

        if self.item.level is None:
            self.fail_reason = 'item in limbo'
            return False

        if self.item.location != item.location:
            self.fail_reason = 'item dropped to incorrect location'
            return False

        if not self.item in get_items(self.item.level):
            self.fail_reason = 'item not in level'
            return False

        self.old_time = get_history_value(item, 'tick')
        self.new_time = item.tick
        if not self.old_time < self.new_time:
            self.fail_reason = 'time did not pass'
            return False

        return True

    def describe_to(self, description):
        """
        Descripe the match

        :param description: description text to append
        :type description: string
        """
        description.append('Character who dropped {0}'
                           .format(self.item.name))

    def describe_mismatch(self, item, mismatch_description):
        """
        Descripe the mismatch

        :item: mismatching item
        :param mismatch_description: description text to append
        :type mismatch_description: string
        """
        if self.fail_reason == 'item not dropped':
            mismatch_description.append('{0} is still holding {1}'
                                        .format(item,
                                                self.item))
        elif self.fail_reason == 'item in limbo':
            mismatch_description.append('{0} is not in any level'
                                        .format(self.item))
        elif self.fail_reason == 'item dropped to incorrect location':
            mismatch_description.append('{0} dropped to {1}, should been {2}'
                                        .format(self.item,
                                                self.item.location,
                                                item.location))
        elif self.fail_reason == 'item not in level':
            mismatch_description.append('{0} is not in level {1}'
                                        .format(self.item,
                                                self.item.level))
        elif self.fail_reason == 'time did not pass':
            mismatch_description.append(
                'Flow of time is incorrect. Before: {0}, after: {1}'
                .format(self.old_time,
                        self.new_time))
        else:
            mismatch_description.append('Unimplemented matcher')


def has_dropped(item):
    """
    Check if character has dropped item
    """
    return HasDropped(item)
