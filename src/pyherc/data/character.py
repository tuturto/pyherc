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
Module for Character related classes
"""
from pyherc.aspects import Logged
from pyherc.rules import MoveParameters, AttackParameters, DrinkParameters
from pyherc.rules import InventoryParameters

class Character(object):
    """
    Represents a character in playing world
    """
    logged = Logged()

    @logged
    def __init__(self, model, action_factory, effects_collection, rng):
        """
        Default constructor

        :param model: model where character acts
        :type model: Model
        :param action_factory: action factory for character to use
        :type action_factory: ActionFactory
        :param effects_collection: collection for effects
        :type effects_collection: EffectsCollection
        :param rng: random number generator
        :type rng: Random
        """
        super(Character, self).__init__()
        # attributes
        self.model = model
        self.__body = None
        self.__finesse = None
        self.__mind = None
        self.name = 'prototype'
        self.race = None
        self.kit = None
        self.__hit_points = None
        self.__max_hp = None
        self.speed = None
        self.inventory = []
        self.weapons = []
        self.feats = []
        #location
        self.level = None
        self.location = ()
        #icon
        self.icon = None
        #internal
        self.tick = 0
        self.short_term_memory = []
        self.item_memory = {}
        self.size = 'medium'
        self.attack = None
        #mimic
        self.mimic_item = None
        self.__active_effects = [] # active effects
        self.action_factory = action_factory
        self.artificial_intelligence = None
        self.__effects_collection = effects_collection
        self.rng = rng

    def __str__(self):
        return self.name

    @logged
    def receive_event(self, event):
        """
        Receives an event from world and enters it into short term memory

        :param event: event to receive
        :type event: Event
        """
        self.short_term_memory.append(event)

    @logged
    def act(self, model):
        """
        Triggers AI of this character

        :param model: model where character is located
        :type model: Model
        """
        self.artificial_intelligence.act(model)

    def __get_hp(self):
        """
        Get current hitpoints

        :returns: hit points
        :rtype: integer
        """
        return self.__hit_points

    def __set_hp(self, hit_points):
        """
        Set current hitpoints

        :param hit_points: hit points to set
        :type hit_points: integer
        """
        self.__hit_points = hit_points

    def __get_body(self):
        """
        Get body attribute

        :returns: Body attribute of this character
        :rtype: integer
        """
        return self.__body

    def __set_body(self, body):
        """
        Set body attribute

        :param body: body attribute to set
        :type body: integer
        """
        self.__body = body

    def __get_finesse(self):
        """
        Get finesse attribute

        :returns: finesse attribute
        :rtype: integer
        """
        return self.__finesse

    def __set_finesse(self, finesse):
        """
        Set finesse attribute

        :param finesse: finesse attribute to set
        :type finesse: integer
        """
        self.__finesse = finesse

    def __get_mind(self):
        """
        Get mind attribute

        :returns: Mind attribute
        :rtype: integer
        """
        return self.__mind

    def __set_mind(self, mind):
        """
        Set mind attribute

        :param mind: mind attribute to set
        :type mind: integer
        """
        self.__mind = mind

    def get_attack(self):
        """
        Return attack attribute of the character

        :returns: Attack value
        :rtype: integer
        """
        return self.attack

    def set_attack(self, attack):
        """
        Set attack attribute of the character

        :param attack: Attack attribute
        :type attack: integer
        """
        self.attack = attack

    def __get_max_hp(self):
        """
        Get maximum HP this character can currently have

        :returns: maximum hit points
        :rtype: integer
        """
        return self.__max_hp

    def __set_max_hp(self, max_hp):
        """
        Set maximum HP this character can currently have

        :param max_hp: maximum hit points
        :type max_hp: integer
        """
        self.__max_hp = max_hp

    @logged
    def identify_item(self, item):
        """
        Identify item

        :param item: item to mark as identified
        :type item: Item
        """
        assert (item != None)
        self.item_memory[item.name] = item.name

    @logged
    def is_proficient(self, weapon):
        """
        Check if this character is proficient with a given weapon

        :param weapon: weapon which proficient requirements should be checked
        :type weapon: Item
        :returns: True if proficient, otherwise False
        :rtype: Boolean
        """
        assert weapon != None

        if weapon.weapon_data == None:
            return True

        if True in [(x.name == 'weapon proficiency'
                    and x.weapon_type == weapon.weapon_data.weapon_type)
                    and (x.weapon_name == None
                         or x.weapon_name == weapon.weapon_data.name)
                    for x in self.feats]:
            return True
        else:
            return False

    def set_mimic_item(self, item):
        """
        Sets item this character can mimic or pretend to be

        :param item: item to mimic
        :type item: Item
        """
        self.mimic_item = item

    def get_mimic_item(self):
        """
        Gets item this character can mimic

        :returns: item to mimic
        :rtype: Item
        """
        return self.mimic_item

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

    @logged
    def execute_action(self, action_parameters):
        """
        Execute action defined by action parameters

        :param action_parameters: parameters controlling creation of the action
        :type action_parameters: ActionParameters
        """
        action = self.create_action(action_parameters)
        action.execute()

    @logged
    def create_action(self, action_parameters):
        """
        Create an action by defined by action parameters

        :param action_parameters: parameters controlling creation of the action
        :type action_parameters: ActionParameters
        :returns: Action
        """
        assert self.action_factory != None

        action = self.action_factory.get_action(action_parameters)

        assert action != None

        return action

    @logged
    def move(self, direction):
        """
        Move this character to specified direction

        :param direction: direction to move
        :type direction: integer
        """
        action = self.action_factory.get_action(
                                                MoveParameters(
                                                                self,
                                                                direction,
                                                                'walk'))
        action.execute()

    @logged
    def is_move_legal(self, direction, movement_mode):
        """
        Check if movement is legal

        :param direction: direction to move
        :type direction: integer
        :param movement_mode: mode of movement
        :type movement_mode: string
        :returns: True if move is legal, False otherwise
        :rtype: Boolean
        """
        action = self.action_factory.get_action(
                                                MoveParameters(
                                                                self,
                                                                direction,
                                                                movement_mode))
        return action.is_legal()

    @logged
    def perform_attack(self, direction):
        """
        Attack to given direction

        :param direction: direction to attack
        :type direction: integer
        """
        if len(self.weapons) == 0:
            attack_type = 'unarmed'
        else:
            attack_type = 'melee'
        action = self.action_factory.get_action(
                                                AttackParameters(
                                                                self,
                                                                direction,
                                                                attack_type,
                                                                self.rng))
        if action != None:
            action.execute()

    @logged
    def drink(self, potion):
        """
        Drink potion

        :param potion: potion to drink
        :type potion: Item
        """
        action = self.action_factory.get_action(
                                                DrinkParameters(
                                                                self,
                                                                potion))
        action.execute()

    @logged
    def pick_up(self, item):
        """
        Pick up item

        :param item: item to pick up
        :type item: Item
        """
        action = self.action_factory.get_action(
                                    InventoryParameters(
                                                        self,
                                                        item,
                                                        'pick up'))
        action.execute()

    def __getstate__(self):
        """
        Override __getstate__ in order to get pickling work
        """
        properties = dict(self.__dict__)
        del properties['logger']
        return properties

    def __setstate__(self, properties):
        """
        Override __setstate__ in order to get pickling work
        """
        self.__dict__.update(properties)

    @logged
    def raise_event(self, event):
        """
        Raise event for other creatures to see

        :param event: event to raise
        :type event: Event
        """
        self.model.raise_event(event)

    @logged
    def add_effect_handle(self, effect):
        """
        Adds an effect handle to an character

        :param effect: effect to add
        :type effect: EffectHandle
        """
        self.__effects_collection.add_effect_handle(effect)

    @logged
    def get_effect_handles(self, trigger = None):
        """
        Get effect handles

        :param trigger: optional trigger type
        :type trigger: string

        :returns: effect handles
        :rtype: [EffectHandle]
        """
        return self.__effects_collection.get_effect_handles(trigger)

    @logged
    def remove_effect_handle(self, handle):
        """
        Remove given handle

        :param handle: handle to remove
        :type handle: EffectHandle
        """
        self.effects_collect.remove_effect_handle(handle)

    @logged
    def add_effect(self, effect):
        """
        Adds effect to this character

        :param effect: Effect to add
        :type effect: Effect
        """
        self.__effects_collection.add_effect(effect)

    @logged
    def get_effects(self):
        """
        Get effects of the character

        :returns: effects
        :rtype: [Effect]
        """
        return self.__effects_collection.get_effects()

    @logged
    def remove_expired_effects(self):
        """
        Remove all effects that have expired
        """
        self.__effects_collection.remove_expired_effects()

    def add_to_tick(self, cost):
        """
        Add cost of action to characters tick,
        while taking characters speed into account

        :param cost: Cost of action in ticks
        :type cost: integer
        """
        self.tick = self.tick + (self.speed * cost)

    hit_points = property(__get_hp, __set_hp)
    """Current hit points of the character"""

    max_hp = property(__get_max_hp, __set_max_hp)
    """Current maximum hit points of the character"""

    body = property(__get_body, __set_body)
    """Body attribute of the character"""

    finesse = property(__get_finesse, __set_finesse)
    """Finesse attribute of the character"""

    mind = property(__get_mind, __set_mind)
    """Mind attribute of the character"""

class Feat(object):
    """
    Represents a feat that a character can have
    """
    def __init__(self, name = None, target = None):
        self.name = name
        self.target = target

class WeaponProficiency(Feat):
    """
    Represents weapon proficiency feats (proficiency, focus, etc.)
    """
    def __init__(self, weapon_type = 'simple', weapon_name = None):
        Feat.__init__(self, weapon_type, weapon_name)

        self.name = 'weapon proficiency'
        self.weapon_type = weapon_type
        self.weapon_name = weapon_name
