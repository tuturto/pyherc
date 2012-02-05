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
Factory related classes are defined here
'''
import logging

class SubActionFactory(object):
    '''
    Factory to handle concrete creation of actions
    '''
    def __init__(self):
        '''
        Constructor for this factory
        '''
        self.action_type = 'default'
        self.logger = logging.getLogger('pyherc.rules.factory.SubActionFactory')
        self.factories = []

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

    def can_handle(self, parameters):
        '''
        Can this factory process these parameters
        @param parameters: Parameters to check
        @returns: True if factory is capable of handling parameters
        '''
        return self.action_type == parameters.action_type


    def get_action(self, parameters):
        '''
        Create an action
        @param parameters: Parameters used to control action creation
        '''
        sub = self.get_sub_factory(parameters)
        return sub.get_action(parameters)
