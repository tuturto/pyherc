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
import types
import logging
import pyHerc.data.tiles
from pyHerc.rules.move.action import MoveAction
from pyHerc.rules.public import SubActionFactory

class MoveFactory(SubActionFactory):
    '''
    Factory for constructing move actions
    '''
    def __init__(self, factories = None):
        '''
        Constructor for this factory
        @param factories: a single Factory or list of Factories to use
        '''
        self.logger = logging.getLogger('pyHerc.rules.move.factories.MoveFactory')
        self.logger.debug('initialising MoveFactory')
        self.action_type = 'move'

        if factories != None:
            if isinstance(factories, types.ListType):
                self.factories = factories
            else:
                self.factories = []
                self.factories.append(factories)

        self.logger.debug('MoveFactory initialised')

    def get_sub_factory(self, parameters):
        '''
        Get sub factory to handle parameters
        @param parameters: Parameters to use for searching the factory
        '''
        self.logger.debug('getting sub factory for ' + str(parameters))
        subs = [x for x in self.factories if x.can_handle(parameters)]

        if len(subs) == 1:
            self.logger.debug('sub factory found: ' + str(subs[0]))
            return subs[0]
        else:
            self.logger.debug('no factory found')
            return None

    def get_action(self, parameters):
        '''
        Create an action
        @param parameters: Parameters used to control action creation
        '''
        sub = self.get_sub_factory(parameters)
        return sub.get_action(parameters)

class WalkFactory(SubActionFactory):
    '''
    Factory for creating walk actions
    '''
    def __init__(self):
        '''
        Constructor for this factory
        '''
        self.logger = logging.getLogger('pyHerc.rules.move.factories.WalkFactory')
        self.logger.debug('initialising WalkFactory')
        self.movement_mode = 'walk'
        self.logger.debug('WalkFactory initialised')

    def __str__(self):
        return 'walk factory'

    def can_handle(self, parameters):
        '''
        Can this factory process these parameters
        @param parameters: Parameters to check
        @returns: True if factory is capable of handling parameters
        '''
        return self.movement_mode == parameters.movement_mode

    def get_action(self, parameters):
        '''
        Create a walk action
        @param parameters: Parameters used to control walk creation
        '''
        location = parameters.character.location
        newLevel = parameters.character.level
        direction = parameters.direction

        if direction == 1:
            newLocation = (location[0], location[1] - 1)
        elif direction == 2:
            newLocation = (location[0] + 1, location[1] - 1)
        elif direction == 3:
            newLocation = (location[0] + 1, location[1])
        elif direction == 4:
            newLocation = (location[0] + 1, location[1] + 1)
        elif direction == 5:
            newLocation = (location[0], location[1] + 1)
        elif direction == 6:
            newLocation = (location[0] - 1, location[1] + 1)
        elif direction == 7:
            newLocation = (location[0] - 1, location[1])
        elif direction == 8:
            newLocation = (location[0] - 1, location[1] - 1)
        elif direction == 9:
            portal = newLevel.get_portal_at(location)
            if portal != None:
                if portal.get_other_end() != None:
                    newLevel = portal.get_other_end().level
                    newLocation = portal.get_other_end().location
                else:
                    #proxy
                    if portal.level_generator != None:
                        #TODO: model parameter
                        portal.generate_level()
                        newLevel = portal.get_other_end().level
                        newLocation = portal.get_other_end().location
                    else:
                        #escaping perhaps?
                        newLevel = None
                        newLocation = None
            else:
                newLevel = parameters.character.level
                newLocation = parameters.character.location

        #is new location blocked?
        if newLevel.get_wall_tile(newLocation[0], newLocation[1]) != pyHerc.data.tiles.WALL_EMPTY:
            newLocation = parameters.character.location

        return MoveAction(parameters.character, newLocation, newLevel)
