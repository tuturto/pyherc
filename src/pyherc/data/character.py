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

"""
Module for Character related classes
"""
from decorator import decorator
from pyherc.aspects import log_debug, log_info
from pyherc.data.new_character import raise_event
from pyherc.data.effects.effectscollection import EffectsCollection
from pyherc.data.inventory import Inventory
from pyherc.data.magic.spellbook import SpellBook
from pyherc.events import (ErrorEvent, HitPointsChangedEvent,
                           SpiritPointsChangedEvent)


@decorator
def guarded_action(wrapped_function, *args, **kwargs):
    """
    Decorator to guard against exceptions in action functions
    """
    try:
        return wrapped_function(*args, **kwargs)
    except Exception:
        self = args[0]
        self.tick = 10
        raise_event(self, ErrorEvent(self))


class Character():
    """
    Represents a character in playing world
    """
    @log_debug
    def __init__(self, model):
        """
        Default constructor

        :param model: model where character acts
        :type model: Model
        """
        super().__init__()
        # attributes
        self.model = model
        self.body = None
        self.finesse = None
        self.mind = None
        self.name = 'prototype'
        self.race = None
        self.kit = None
        self.hit_points = None
        self.max_hp = None
        self.__spirit = 100
        self.max_spirit = 100
        self.speed = None
        self.inventory = Inventory()
        self.feats = []
        #location
        self.level = None
        self.location = ()
        #icon
        self.icon = None
        #internal
        self.tick = 0
        self.short_term_memory = []
        self.event_listeners = []
        self.update_listeners = []
        self.item_memory = {}
        self.size = 'medium'
        self.attack = None

        self.__active_effects = []
        self.artificial_intelligence = None
        self.__effects_collection = EffectsCollection()
        self.__spellbook = SpellBook()

    def __str__(self):
        return self.name

    @guarded_action
    @log_info
    def act(self, model, action_factory, rng):
        """
        Triggers AI of this character

        :param model: model where character is located
        :type model: Model
        :param action_factory: factory for creating actions
        :type action_factory: ActionFactory
        :param rng: random number generator
        :type rng: Random
        """
        self.artificial_intelligence.act(model,
                                         action_factory,
                                         rng)

    def __get_spirit(self):
        """
        Current spirit points
        """
        return self.__spirit

    def __set_spirit(self, spirit):
        old_spirit = self.__spirit
        new_spirit = spirit

        self.__spirit = spirit

        raise_event(self,
                    SpiritPointsChangedEvent(character=self,
                                             old_spirit=old_spirit,
                                             new_spirit=new_spirit))

    @log_debug
    def identify_item(self, item):
        """
        Identify item

        :param item: item to mark as identified
        :type item: Item
        """
        assert item is not None
        self.item_memory[item.name] = item.name

    def get_location(self):
        """
        Returns location of this character

        :returns: location
        :rtype: (integer, integer)
        """
        return self.location

    def set_location(self, location):
        """
        Sets location of this character

        :param location: location to set
        :type location: (integer, integer)
        """
        self.location = location

    @guarded_action
    @log_info
    def execute_action(self, action_parameters, action_factory):
        """
        Execute action defined by action parameters

        :param action_parameters: parameters controlling creation of the action
        :type action_parameters: ActionParameters
        :param action_factory: factory to create actions
        :type action_factory: ActionFactory
        """
        action = self.create_action(action_parameters,
                                    action_factory)
        action.execute()

    @log_debug
    def create_action(self, action_parameters, action_factory):
        """
        Create an action by defined by action parameters

        :param action_parameters: parameters controlling creation of the action
        :type action_parameters: ActionParameters
        :param action_factory: factory to create actions
        :type action_factory: ActionFactory
        :returns: Action
        """
        action = action_factory.get_action(action_parameters)

        assert action is not None

        return action

    @log_debug
    def add_effect_handle(self, effect):
        """
        Adds an effect handle to an character

        :param effect: effect to add
        :type effect: EffectHandle

        .. versionadded:: 0.4
        """
        self.__effects_collection.add_effect_handle(effect)

    @log_debug
    def get_effect_handles(self, trigger=None):
        """
        Get effect handles

        :param trigger: optional trigger type
        :type trigger: string

        :returns: effect handles
        :rtype: [EffectHandle]

        .. versionadded:: 0.4
        """
        return self.__effects_collection.get_effect_handles(trigger)

    @log_debug
    def remove_effect_handle(self, handle):
        """
        Remove given handle

        :param handle: handle to remove
        :type handle: EffectHandle

        .. versionadded:: 0.4
        """
        self.__effects_collection.remove_effect_handle(handle)

    @log_debug
    def add_effect(self, effect):
        """
        Adds effect to this character

        :param effect: Effect to add
        :type effect: Effect

        .. note:: Multiples of same type of effect are not added
        .. versionadded:: 0.4
        """
        if not effect.multiple_allowed:
            if not self.__effects_collection.has_effect(effect):
                self.__effects_collection.add_effect(effect)
                raise_event(self, effect.get_add_event())
        else:
            self.__effects_collection.add_effect(effect)
            raise_event(self, effect.get_add_event())

    @log_debug
    def get_effects(self):
        """
        Get effects of the character

        :returns: effects
        :rtype: [Effect]

        .. versionadded:: 0.4
        """
        return self.__effects_collection.get_effects()

    @log_debug
    def remove_expired_effects(self):
        """
        Remove all effects that have expired

        .. versionadded:: 0.4
        """
        removed = self.__effects_collection.get_expired_effects()

        if len(removed) > 0:
            self.__effects_collection.remove_expired_effects()
            for effect in removed:
                raise_event(self, effect.get_removal_event())

    @log_debug
    def add_to_tick(self, cost):
        """
        Add cost of action to characters tick,
        while taking characters speed into account

        :param cost: Cost of action in ticks
        :type cost: integer
        """
        self.tick = self.tick + (self.speed * cost)

    @log_debug
    def add_domain_level(self, domain, level=None):
        """
        Add level to a spell domain

        :param domain: name of domain to learn
        :type domain: string
        :param level: amount to increment the level
        :type level: int

        .. note:: if level is None, current level is incremented by one

        .. versionadded:: 0.10
        """
        self.__spellbook.add_domain_level(domain, level)

    @log_debug
    def get_domain_level(self, domain):
        """
        Get current level of a given domain

        :param domain: name of the domain
        :type domain: String
        :returns: current level, 0 if character does not know the domain
        :rtype: int

        .. versionadded:: 0.10
        """
        return self.__spellbook.get_domain_level(domain)

    @log_debug
    def add_spell_entry(self, entry):
        """
        Add spell entry into characters spellbook

        :param entry: entry to add
        :type entry: SpellEntry

        .. versionadded:: 0.10
        """
        self.__spellbook.add_spell_entry(entry)

    @log_debug
    def get_known_spells(self):
        """
        Get a list of known spells

        :returns: list of known spells
        :rtype: [SpellEntry]
        """
        return self.__spellbook.get_known_spells()

    @log_debug
    def get_location_at_direction(self, direction):
        """
        Get location next to this character at given direction

        :param direction: direction to check
        :type direction: int
        :returns: coordinates of location
        :rtype: (int, int)

        .. note:: values 1 to 8 are supported for direction
        """
        assert direction <= 8
        assert direction >= 1

        offset = [(0, 0),
                  (0, -1), (1, -1), (1, 0), (1, 1),
                  (0, 1), (-1, 1), (-1, 0), (-1, -1)]

        return tuple(x for x in
                     map(sum, zip(self.location, offset[direction])))

    spirit = property(__get_spirit, __set_spirit)


class Feat():
    """
    Represents a feat that a character can have
    """
    @log_debug
    def __init__(self, name=None, target=None):

        super().__init__()
        self.name = name
        self.target = target


class WeaponProficiency(Feat):
    """
    Represents weapon proficiency feats (proficiency, focus, etc.)
    """
    @log_debug
    def __init__(self, weapon_type='simple', weapon_name=None):

        super().__init__(weapon_type, weapon_name)

        self.name = 'weapon proficiency'
        self.weapon_type = weapon_type
        self.weapon_name = weapon_name
