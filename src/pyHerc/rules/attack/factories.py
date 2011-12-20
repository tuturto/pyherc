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
from pyHerc.rules.attack.action import AttackAction
from pyHerc.rules.attack.unarmed import UnarmedToHit
from pyHerc.rules.attack.unarmed import UnarmedDamage
from pyHerc.rules.factory import SubActionFactory

class UnarmedCombatFactory():
    '''
    Factory for producing unarmed combat actions
    '''

    def __init__(self):
        '''
        Constructor for this factory
        '''
        self.logger = logging.getLogger('pyHerc.rules.attack.factories.UnarmedCombatFactory')
        self.logger.debug('initialising UnarmedCombatFactory')
        self.attack_type = 'unarmed'
        self.logger.debug('UnarmedCombatFactory initialised')

    def __getstate__(self):
        '''
        Override __getstate__ in order to get pickling work
        '''
        d = dict(self.__dict__)
        del d['logger']
        return d

    def __setstate__(self, d):
        '''
        Override __setstate__ in order to get pickling work
        '''
        self.__dict__.update(d)
        self.logger = logging.getLogger('pyHerc.rules.attack.factories.UnarmedCombatFactory')

    def __str__(self):
        return 'unarmed combat factory'

    def can_handle(self, parameters):
        '''
        Can this factory process these parameters
        @param parameters: Parameters to check
        @returns: True if factory is capable of handling parameters
        '''
        return self.attack_type == parameters.attack_type

    def get_action(self, parameters):
        '''
        Create a attack action
        @param parameters: Parameters used to control attack creation
        '''
        self.logger.debug('Creating an unarmed attack')

        attacker = parameters.attacker
        target = parameters.target

        attack = AttackAction('unarmed',
                        UnarmedToHit(attacker, target,
                                    parameters.random_number_generator),
                        UnarmedDamage(attacker.get_attack()),
                        attacker,
                        target,
                        parameters.model)

        return attack

class AttackFactory(SubActionFactory):
    '''
    Factory for constructing attack actions
    '''
    def __init__(self, factories):
        '''
        Constructor for this factory
        '''
        self.logger = logging.getLogger('pyHerc.rules.attack.factories.AttackFactory')
        self.logger.debug('initialising AttackFactory')
        self.action_type = 'attack'

        if isinstance(factories, types.ListType):
            self.factories = factories
        else:
            self.factories = []
            self.factories.append(factories)

        self.logger.debug('AttackFactory initialised')
