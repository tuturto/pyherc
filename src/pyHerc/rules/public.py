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

import types
from pyHerc.rules.move.factories import MoveFactory
from pyHerc.rules.attack.factories import AttackFactory

'''
Public interface for action subsystem

Classes:
ActionFactory - Class used to contruct Action objects
ActionParameters - Class used to guide Action construction

AttackParameters - Class used to guide contruction of attack related actions
'''

class ActionFactory():
    '''
    Object for creating actions
    '''

    def __init__(self, factories = [MoveFactory(), AttackFactory()]):
        '''
        Construct ActionFactory
        @param factories: a single Factory or list of Factories to use
        '''
        if factories != None:
            if isinstance(factories, types.ListType):
                self.factories = factories
            else:
                self.factories = []
                self.factories.append(factories)

    def get_action(self, parameters):
        '''
        Create an action
        @param parameters: Parameters used to control action creation
        '''
        factory = self.get_sub_factory(parameters)
        return factory.get_action(parameters)

    def get_sub_factories(self):
        '''
        Get all sub factories
        @returns: List of sub factories
        '''
        return self.factories

    def get_sub_factory(self, parameters):
        '''
        Get sub factory to handle parameters
        @param parameters: Parameters to use for searching the factory
        '''
        subs = [x for x in self.factories if x.can_handle(parameters)]

        if len(subs) == 1:
            return subs[0]
        else:
            return None

class ActionParameters():
    '''
    Object for controlling action creation
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        self.action_type = 'default'

class AttackParameters(ActionParameters):
    '''
    Object for controlling attack action creation
    '''
    def __init__(self, attacker, target, attack_type,
                        random_number_generator = None):
        '''
        Construct AttackParameters
        @param attacker: Character doing an attack
        @param target: Character being attacked
        @param attack_type: type of attack to perform
        '''
        ActionParameters.__init__(self)

        self.action_type = 'attack'
        self.attacker = attacker
        self.target = target
        self.attack_type = attack_type
        self.rng = random_number_generator

    def __str__(self):
        return 'attack with attack type of ' + self.attack_type

class MoveParameters(ActionParameters):
    '''
    Object for controlling move action creation
    '''
    def __init__(self, character, direction, movement_mode):
        '''
        Construct move parameters
        @param character: Character moving
        @param direction: Direction of the move
        @param movement_mode: Mode of movement
        '''
        ActionParameters.__init__(self)

        self.action_type = 'move'
        self.character = character
        self.direction = direction
        self.movement_mode = movement_mode

    def __str__(self):
        return 'move with movement mode of ' + self.movement_mode

