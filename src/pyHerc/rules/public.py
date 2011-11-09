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

'''
Public interface for action subsystem

Classes:
    Action - Represents a single action taken by a character
    ActionFactory - Class used to contruct Action objects
    ActionParameters - Class used to guide Action construction

    AttackParameters - Class used to guide contruction of attack related actions
'''

class Action():
    '''
    Object representing an action taken by a character
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        pass

    def execute(self):
        '''
        Executes the action
        '''
        pass

class ActionFactory():
    '''
    Object for creating actions
    '''

    def __init__(self, factories):
        '''
        Construct ActionFactory
        @param factories: a single Factory or list of Factories to initialise
        '''
        if isinstance(factories, types.ListType):
            self.factories = [factory() for factory in factories]
        else:
            self.factories = []
            self.factories.append(factories())

    def get_action(self, parameters):
        '''
        Create an action
        @param parameters: Parameters used to control action creation
        '''
        return self.factories[0].get_action(parameters)

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

class SubActionFactory():
    '''
    Factory to handle concrete creation of actions
    '''
    def __init__(self):
        '''
        Constructor for this factory
        '''
        self.action_type = 'default'

    def can_handle(self, parameters):
        '''
        Can this factory process these parameters
        @param parameters: Parameters to check
        @returns: True if factory is capable of handling parameters
        '''
        return self.action_type == parameters.action_type

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
    def __init__(self, attacker, defender, attack_type):
        '''
        Construct AttackParameters
        @param attacker: Character doing an attack
        @param defender: Character being attacked
        @param attack_type: type of attack to perform
        '''
        ActionParameters.__init__(self)

        self.action_type = 'attack'
        self.attacked = attacker
        self.defender = defender
        self.attack_type = attack_type
