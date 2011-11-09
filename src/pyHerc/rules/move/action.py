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
Module defining classes related to MoveAttack
'''
from pyHerc.rules.public import Action

class MoveAction(Action):
    '''
    Action for moving
    '''
    def __init__(self, character, new_location):
        '''
        Default constructor
        @param character: Character moving
        @param new_location: Location to move
        '''
        self.character = character
        self.new_location = new_location

    def execute(self):
        '''
        Executes this Move
        '''
        pass
