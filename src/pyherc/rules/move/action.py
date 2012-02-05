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

'''
Module defining classes related to MoveAttack
'''
import logging
import pyherc.rules.time

class MoveAction():
    '''
    Action for moving
    '''
    def __init__(self, character, new_location, new_level = None):
        '''
        Default constructor
        @param character: Character moving
        @param new_location: Location to move
        '''
        self.logger = logging.getLogger('pyherc.rules.move.action.MoveAction')
        self.logger.debug('Initialising move action')
        self.character = character
        self.new_location = new_location
        self.new_level = new_level
        self.model = None
        self.logger.debug('Move action initialised')

    def execute(self):
        '''
        Executes this Move
        '''
        self.logger.debug('Executing move')
        if self.is_legal():
            self.character.location = self.new_location
            if self.new_level != None:
                self.character.level = self.new_level
            #TODO: refactor to be pluggable
            self.character.tick = pyherc.rules.time.get_new_tick(self.character, 2)
        else:
            self.logger.warn('Tried to execute illegal move')
            self.character.tick = pyherc.rules.time.get_new_tick(self.character, 2)
        self.logger.debug('Move executed')

    def is_legal(self):
        '''
        Check if the move is possible to perform
        @returns: True if move is possible, false otherwise
        '''
        location_ok = False
        if self.new_level != None:
            if self.new_level.walls[self.new_location[0]][self.new_location[1]] == pyherc.data.tiles.WALL_EMPTY:
                #check for other creatures and such
                location_ok = True
                creatures = self.new_level.creatures[:]
                #TODO: take PC into consideration
                for creature in creatures:
                    if creature.location == self.new_location:
                        location_ok = False
            else:
                location_ok = False
        else:
            #TODO: is this player escaping?
            pass

        return location_ok

class WalkAction(MoveAction):
    '''
    Action for walking
    '''
    def execute(self):
        '''
        Execute this move
        '''
        self.logger.debug('Executing walk')

        MoveAction.execute(self)

        self.logger.debug('Walk executed')
