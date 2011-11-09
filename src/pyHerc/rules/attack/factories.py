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
Attack related factories are defined here
'''

from pyHerc.rules.attack.action import AttackAction
from pyHerc.rules.public import SubActionFactory

class AttackFactory(SubActionFactory):
    '''
    Factory for constructing attack actions
    '''
    def __init__(self):
        '''
        Constructor for this factory
        '''
        self.action_type = 'attack'

    def get_action(self, parameters):
        '''
        Create an action
        @param parameters: Parameters used to control action creation
        '''
        return AttackAction(None, None)

class ToHitFactory():
    '''
    Factory for constructing ToHit objects
    '''
    pass

class DamageFactory():
    '''
    Factory for constructing Damage objects
    '''
    pass
