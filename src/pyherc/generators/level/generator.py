#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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

"""
Classs needed for generating levels
"""

import logging
from pyherc.generators import ItemGenerator
from pyherc.generators import CreatureGenerator
from pyherc.generators.level.config import LevelGeneratorFactoryConfig
from pyherc.data import Level

class LevelGeneratorFactory:
    """
    Class used to contruct different kinds of level generators
    """
    def __init__(self, action_factory, configuration, random_generator):
        """
        Default constructor

        Args:
            action_factory: ActionFactory to pass to the generator
            configuration: Configuration for factory
            random_generator: Random number generator
        """
        self.logger = logging.getLogger('pyherc.generators.level.crypt.LevelGeneratorFactory') #pylint: disable=c0301
        self.action_factory = action_factory
        self.level_partitioners = configuration.level_partitioners
        self.room_generators = configuration.room_generators
        self.decorators = configuration.decorators
        self.stair_adder = None
        self.random_generator = random_generator
        self.size = configuration.size

    def get_generator(self, level_type):
        """
        Get LevelGenerator for given level

        Args:
            level_type: type of level to generate

        Returns:
            configured LevelGenerator
        """
        partitioner = self.random_generator.choice(self.level_partitioners)

        matching_room_generators = [x for x in self.room_generators
                                    if level_type in x.level_types]

        if len(matching_room_generators) > 0:
            room = self.random_generator.choice(matching_room_generators)
        else:
            error_message = "No room generator found for type {0}".format(
                                                        level_type)
            self.logger.error(error_message)
            raise RuntimeError(error_message)

        decorator = self.random_generator.choice(self.decorators)

        return LevelGenerator(self.action_factory,
                                        partitioner,
                                        room,
                                        decorator,
                                        self.stair_adder,
                                        self.random_generator,
                                        self.size)

class LevelGenerator:
    """
    Class used to generate levels
    """
    def __init__(self, action_factory, partitioner, room_generator,
                 decorator, stair_adder, random_generator, size):
        """
        Default constructor

        Args:
            action_factory: ActionFactory instance
            partitioner: LevelPartitioner to use
            room_generator: RoomGenerator to use
            decorator: LevelDecorator to use
            stair_adder: PortalAdder to use
            random_generator: Random number generator
            size: Size of the level to create
        """
        self.logger = logging.getLogger('pyherc.generators.level.crypt.LevelGenerator') #pylint: disable=C0301
        self.item_generator = ItemGenerator()
        self.creature_generator = CreatureGenerator(action_factory)
        self.random_generator = random_generator

        self.action_factory = action_factory
        self.partitioner = partitioner
        self.room_generator = room_generator
        self.decorator = decorator
        self.stair_adder = stair_adder
        self.size = size

    def __getstate__(self):
        """
        Override __getstate__ in order to get pickling work
        """
        d = dict(self.__dict__)
        del d['logger']
        return d

    def __setstate__(self, d):
        """
        Override __setstate__ in order to get pickling work
        """
        self.__dict__.update(d)
        self.logger = logging.getLogger('pyherc.generators.level.crypt.LevelGenerator') #pylint: disable=C0301

    def generate_level(self, portal, model, new_portals = 0,
                                        level=1, room_min_size = (2, 2)):
        """
        Generate level
        """
        self.logger.debug('creating a new level')
        new_level = Level(self.size)

        self.logger.debug('partitioning level')
        sections = self.partitioner.partition_level(new_level, 4, 3)

        self.logger.debug('generating rooms')
        for section in sections:
            self.room_generator.generate_room(section)

        self.decorator.decorate_level(new_level)

        self.stair_adder.add_stairs(new_level, portal)

        # add monsters
        # add items

        self.logger.debug(new_level.dump_string())

        return new_level
