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
import logging
import pyHerc.rules.time
from pyHerc.rules.public import Action

class MoveAction(Action):
    '''
    Action for moving
    '''
    def __init__(self, character, new_location, new_level = None):
        '''
        Default constructor
        @param character: Character moving
        @param new_location: Location to move
        '''
        self.logger = logging.getLogger('pyHerc.rules.move.action.MoveAction')
        self.logger.debug('Initialising move action')
        self.character = character
        self.new_location = new_location
        self.new_level = new_level
        self.logger.debug('Move action initialised')

    def execute(self):
        '''
        Executes this Move
        '''
        self.logger.debug('Executing move')
        self.character.location = self.new_location
        if self.new_level != None:
            self.character.level = self.new_level
        #TODO: refactor to be pluggable
        self.character.tick = pyHerc.rules.time.get_new_tick(self.character, 2)
        self.logger.debug('Move executed')

class WalkAction(MoveAction):
    '''
    Action for walking
    '''
    def execute(self):
        '''
        Execute this move
        '''
        MoveAction.execute(self)
        self.logger.debug('Executing walk')
        pass
        self.logger.debug('Walk executed')
