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

from pyHerc.rules.move.action import MoveAction
from pyHerc.rules.public import SubActionFactory

class MoveFactory(SubActionFactory):
    '''
    Factory for constructing move actions
    '''
    def __init__(self):
        '''
        Constructor for this factory
        '''
        self.action_type = 'move'

    def get_action(self, parameters):
        '''
        Create an action
        @param parameters: Parameters used to control action creation
        '''
        return MoveAction(None, None)
