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
Public interface for action subsystem

Classes:
    Action - Represents a single action taken by a character
    ActionFactory - Class used to contruct Action objects
    ActionParameters - Class used to guide Action construction

    AttackParameters - Class used to guide contruction of attack related actions
'''

import pyHerc.rules.attack.action

class Action():
    '''
    Object representing an action taken by a character
    '''
    pass

class ActionFactory():
    '''
    Object for creating actions
    '''

    def get_action(self, parameters):
        '''
        Create an action
        @param parameters: Parameters used to control action creation
        '''
        #TODO: hard coded for now
        return pyHerc.rules.attack.action.AttackAction(None, None)

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


