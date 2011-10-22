#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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
        self.endCondition = 0

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

    def __init__(self):
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
        self.maxHp = None
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
        self.shortTermMemory = []
        self.itemMemory = {}

    def __str__(self):
        return self.name

    def receive_event(self, event):
        """
        Receives an event from world and enters it into short term memory
        """
        self.shortTermMemory.append(event)

    def get_max_HP(self):
        """
        Get maximum HP this character can currently have
        """
        return self.maxHp

    def identify_item(self, item):
        """
        Identify item
        @param item: item to mark as identified
        """
        assert (item != None)
        self.itemMemory[item.name] = item.name

    def is_proficient(self, weapon):
        '''
        Check if this character is proficient with a given weapon
        @param weapon: weapon which proficient requirements should be checked
        @returns: True if proficient, otherwise False
        '''
        assert weapon != None

        if weapon.weaponData == None:
            return True

        check_proficiency = lambda x: ((x.name == 'weapon proficiency'
                                   and x.weapon_type == weapon.weaponData.weapon_type)
                                   and (x.weapon_name == None
                                        or x.weapon_name == weapon.weaponData.name))

        if True in map(check_proficiency, self.feats):
            return True
        else:
            return False

class Damage:
    """
    Damage done in combat
    """
    def __init__(self, amount = 0, type = 'bludgeoning', magicBonus = 0):
        self.amount = amount
        self.type = type
        self.magicBonus = magicBonus

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
        self.name = 'weapon proficiency'
        self.weapon_type = weapon_type
        self.weapon_name = weapon_name
