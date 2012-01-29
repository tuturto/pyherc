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
import random
from pyHerc.generators import ItemGenerator
from pyHerc.generators import CreatureGenerator

class CryptGeneratorFactory:
    '''
    Class used to contruct different kinds of crypt generators
    '''
    def __init__(self, action_factory, level_configurations):
        '''
        Default constructor

        @param action_factory: ActionFactory to pass to the generator
        @param level_configurations: List of LevelGeneratorConfiguration objects
        '''
        self.logger = logging.getLogger('pyHerc.generators.level.crypt.CryptGeneratorFactory')
        self.action_factory = action_factory
        self.level_configurations = level_configurations

    def get_generator(self, level, random_generator = random.Random()):
        '''
        Get CryptGenerator for given crypt level
        @param level: current crypt level
        @param random_generator: Optional random number generator
        '''
        return CryptGenerator(self.action_factory,
                                        self.level_configurations[level - 1],
                                        random_generator)

class CryptGenerator:
    '''
    Class used to generate crypts
    '''
    def __init__(self, action_factory, configuration, random_generator):
        '''
        Default constructor
        @param action_factory: ActionFactory instance
        @param configuration: LevelGeneratorConfiguration
        '''
        self.logger = logging.getLogger('pyHerc.generators.level.crypt.CryptGenerator')
        self.item_generator = ItemGenerator()
        self.creature_generator = CreatureGenerator(action_factory)
        self.random_generator = random_generator

        self.action_factory = action_factory
        self.level_partitioners = configuration.level_partitioners

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
        '''
        Generate crypt level
        '''
        # partition level
        partitioner = self.random_generator.choice(self.level_partitioners)
        partitioner.partition_level()
        # generate rooms
        # decorate level
        # add stairs
        # add monsters
        # add items
