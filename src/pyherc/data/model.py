#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2011 Tuukka Turto
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
Module for Model related classes

Classes:
    Model
    Character
    Damage
    Feat
    WeaponProficiency
"""

import logging
import random
from pyherc.aspects import Logged
from pyherc.rules import MoveParameters, AttackParameters, DrinkParameters

class Model:
    """
    Represents playing world
    """
    logged = Logged()

    @logged
    def __init__(self):
        """
        Default constructor
        """
        self.dungeon = None
        self.player = None
        self.config = None
        self.tables = None
        self.end_condition = 0
        self.logger = logging.getLogger('pyherc.data.model.Model')

    def __getstate__(self):
        '''
        Override __getstate__ in order to get pickling work
        '''
        properties = dict(self.__dict__)
        del properties['logger']
        return properties

    def __setstate__(self, properties):
        '''
        Override __setstate__ in order to get pickling work
        '''
        self.__dict__.update(properties)
        self.logger = logging.getLogger('pyherc.data.model.Model')

    @logged
    def raise_event(self, event):
        """
        Relays event to creatures

        Args:
            event: event to relay
        """
        if event['level'] != None:
            for creature in event['level'].creatures:
                creature.receive_event(event)

class Character(object):
    """
    Represents a character in playing world
    """
    logged = Logged()

    @logged
    def __init__(self, action_factory):
        """
        Default constructor
        """
        super(Character, self).__init__()
        # attributes
        self.__body = None
        self.__finesse = None
        self.__mind = None
        self.name = 'prototype'
        self.race = None
        self.kit = None
        self.__hit_points = None
        self.max_hp = None
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
        self.effects = []
        self.action_factory = action_factory
        self.artificial_intelligence = None
        self.rng = random.Random()
        self.logger = logging.getLogger('pyherc.data.model.Character')

    def __str__(self):
        return self.name

    @logged
    def receive_event(self, event):
        """
        Receives an event from world and enters it into short term memory
        """
        self.short_term_memory.append(event)

    @logged
    def act(self, model):
        """
        Triggers AI of this character
        """
        self.artificial_intelligence.act(model)

    def __get_hp(self):
        """
        Get current hitpoints
        """
        return self.__hit_points

    def __set_hp(self, hit_points):
        """
        Set current hitpoints
            hit_points: hit points to set
        """
        self.__hit_points = hit_points

    def __get_body(self):
        """
        Get body attribute

        Returns:
            Body attribute of this character
        """
        return self.__body

    def __set_body(self, body):
        """
        Set body attribute

        Args:
            body: body attribute to set
        """
        self.__body = body

    def __get_finesse(self):
        """
        Get finesse attribute
        @returns: finesse attribute
        """
        return self.__finesse

    def __set_finesse(self, finesse):
        """
        Set finesse attribute
        @param finesse: finesse attribute to set
        """
        self.__finesse = finesse

    def __get_mind(self):
        """
        Get mind attribute
        @returns: Mind attribute
        """
        return self.__mind

    def __set_mind(self, mind):
        """
        Set mind attribute
        @param mind: mind attribute to set
        """
        self.__mind = mind

    def get_attack(self):
        """
        Return attack attribute of the character
        @returns: Attack value
        """
        return self.attack

    def set_attack(self, attack):
        """
        Set attack attribute of the character
        @param attack: Attack attribute
        """
        self.attack = attack

    def get_max_hp(self):
        """
        Get maximum HP this character can currently have
        """
        return self.max_hp

    @logged
    def identify_item(self, item):
        """
        Identify item

        Args:
            item: item to mark as identified
        """
        assert (item != None)
        self.item_memory[item.name] = item.name

    @logged
    def is_proficient(self, weapon):
        """
        Check if this character is proficient with a given weapon

        Args:
        weapon: weapon which proficient requirements should be checked

        Returns:
            True if proficient, otherwise False
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
        @param item: item to mimic
        """
        self.mimic_item = item

    def get_mimic_item(self):
        """
        Gets item this character can mimic
        @returns: item to mimic
        """
        return self.mimic_item

    def get_location(self):
        """
        Returns location of this character
        @returns: location
        """
        return self.location

    def set_location(self, location):
        """
        Sets location of this character
        @param location: location to set
        """
        self.location = location

    @logged
    def execute_action(self, action_parameters):
        """
        Execute action defined by action parameters

        Args:
            action_parameters: parameters controlling creation of the action
        """
        action = self.create_action(action_parameters)
        action.execute()

    @logged
    def create_action(self, action_parameters):
        """
        Create an action by defined by action parameters

        Args:
            action_parameters: parameters controlling creation of the action

        Returns:
            Action
        """
        assert self.action_factory != None

        action = self.action_factory.get_action(action_parameters)

        assert action != None

        return action

    @logged
    def move(self, direction):
        """
        Move this character to specified direction

        Args:
            direction: direction to move
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

        Args:
            direction: direction to move
            movement_mode: mode of movement

        Returns:
            True if move is legal, False otherwise
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

        Args:
            direction: direction to attack
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

        Args:
            potion: Item to drink
        """
        action = self.action_factory.get_action(
                                                DrinkParameters(
                                                                self,
                                                                potion))
        action.execute()

    def __getstate__(self):
        '''
        Override __getstate__ in order to get pickling work
        '''
        properties = dict(self.__dict__)
        del properties['logger']
        return properties

    def __setstate__(self, properties):
        '''
        Override __setstate__ in order to get pickling work
        '''
        self.__dict__.update(properties)
        self.logger = logging.getLogger('pyherc.data.model.Character')

    @logged
    def raise_event(self, event):
        """
        Raise event for other creatures to see
        """
        self.action_factory.model.raise_event(event)

    @logged
    def add_effect(self, effect):
        """
        Adds effect to this character

        Args:
            effect: Effect to add
        """
        assert effect != None
        self.effects.append(effect)

    hit_points = property(__get_hp, __set_hp)
    body = property(__get_body, __set_body)
    finesse = property(__get_finesse, __set_finesse)
    mind = property(__get_mind, __set_mind)

class Damage:
    """
    Damage done in combat
    """
    def __init__(self, amount = 0, damage_type = 'bludgeoning',
                        magic_bonus = 0):
        self.amount = amount
        self.damage_type = damage_type
        self.magic_bonus = magic_bonus

class Feat:
    '''
    Represents a feat that a character can have
    '''
    def __init__(self, name = None, target = None):
        self.name = name
        self.target = target

class WeaponProficiency(Feat):
    '''
    Represents weapon proficiency feats (proficiency, focus, etc.)
    '''
    def __init__(self, weapon_type = 'simple', weapon_name = None):
        Feat.__init__(self, weapon_type, weapon_name)

        self.name = 'weapon proficiency'
        self.weapon_type = weapon_type
        self.weapon_name = weapon_name

class MimicData():
    '''
    Represents mimicing character
    '''
    def __init__(self, character):
        self.fov_matrix = []
        self.character = character

    def get_character(self):
        '''
        Get mimicing character
        @returns: Character
        '''
        return self.character

    def set_character(self, character):
        '''
        Set character mimicing this item
        @param character: Character to set
        '''
        self.character = character

