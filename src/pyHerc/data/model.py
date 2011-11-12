#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2011 Tuukka Turto
#
#   This file is part of pyHerc.
#
#   pyHerc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyHerc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyHerc.  If not, see <http://www.gnu.org/licenses/>.

'''
Module for Model related classes

Classes:
    Model
    Character
    Damage
    Feat
    WeaponProficiency
'''

import logging

class Model:
    """
    Represents playing world
    """

    def __init__(self):
        self.logger = logging.getLogger('pyHerc.data.model.Model')
        self.dungeon = None
        self.player = None
        self.config = None
        self.tables = None
        self.end_condition = 0

        self.logger.info('loading config')
        self.load_config()

    def load_config(self):
        """
        Loads config
        """
        self.config = {}
        self.config['level'] = {}
        self.config['level']['size']  = (80,  21)

    def raise_event(self, event):
        """
        Relays event to creatures
        @param event: event to relay
        """
        self.logger.debug('raising event:' + event.__str__())
        #TODO: filter events
        if event['level'] != None:
            for creature in event['level'].creatures:
                creature.receive_event(event)

        if self.player != None:
            self.player.receive_event(event)

class Character:
    """
    Represents a character in playing world
    """

    def __init__(self, action_factory):
        # attributes
        self.str = None
        self.dex = None
        self.con = None
        self.int = None
        self.wis = None
        self.cha = None
        self.name = 'prototype'
        self.race = None
        self.kit = None
        self.hp = None
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
        self.action_factory = action_factory

    def __str__(self):
        return self.name

    def receive_event(self, event):
        """
        Receives an event from world and enters it into short term memory
        """
        self.short_term_memory.append(event)

    def get_hp(self):
        '''
        Get current hitpoints
        '''
        return self.hp

    def get_max_hp(self):
        """
        Get maximum HP this character can currently have
        """
        return self.max_hp

    def identify_item(self, item):
        """
        Identify item
        @param item: item to mark as identified
        """
        assert (item != None)
        self.item_memory[item.name] = item.name

    def is_proficient(self, weapon):
        '''
        Check if this character is proficient with a given weapon
        @param weapon: weapon which proficient requirements should be checked
        @returns: True if proficient, otherwise False
        '''
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
        '''
        Sets item this character can mimic or pretend to be
        @param item: item to mimic
        '''
        self.mimic_item = item

    def get_mimic_item(self):
        '''
        Gets item this character can mimic
        @returns: item to mimic
        '''
        return self.mimic_item

    def get_location(self):
        '''
        Returns location of this character
        @returns: location
        '''
        return self.location

    def set_location(self, location):
        '''
        Sets location of this character
        @param location: location to set
        '''
        self.location = location

    def execute_action(self, action_parameters):
        '''
        Execute action defined by action parameters
        @param action_parameters: parameters controlling creation of the action
        '''
        if self.action_factory != None:
            action = self.action_factory.get_action(action_parameters)
            action.execute()

class Damage:
    """
    Damage done in combat
    """
    def __init__(self, amount = 0, damage_type = 'bludgeoning', magic_bonus = 0):
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

