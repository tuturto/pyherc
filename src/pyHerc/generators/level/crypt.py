#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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

import logging
from pyHerc.generators import ItemGenerator
from pyHerc.generators import CreatureGenerator

class CryptGeneratorFactory:
    '''
    Class used to contruct different kinds of crypt generators
    '''
    def __init__(self, action_factory):
        '''
        Default constructor

        @param action_factory: ActionFactory to pass to the generator
        '''
        self.logger = logging.getLogger('pyHerc.generators.level.crypt.CryptGeneratorFactory')
        self.action_factory = action_factory

    def get_generator(self, level):
        '''
        Get CryptGenerator for given crypt level
        '''
        return CryptGenerator(self.action_factory)

class CryptGenerator:
    '''
    Class used to generate crypts
    '''
    def __init__(self, action_factory):
        self.logger = logging.getLogger('pyHerc.generators.level.crypt.CryptGenerator')
        self.item_generator = ItemGenerator()
        self.creature_generator = CreatureGenerator(action_factory)

        self.partitioners = []
        self.room_generators = []

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
        self.logger = logging.getLogger('pyHerc.generators.level.crypt.CryptGenerator')

    def generate_level(self, portal, model, new_portals = 0, level=1, room_min_size = (2, 2)):
        pass
