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
        self.portal_adders = configuration.portal_adders
        self.item_adders = configuration.item_adders
        self.creature_adders = configuration.creature_adders
        self.size = configuration.size
        self.random_generator = random_generator

    def get_generator(self, level_type):
        """
        Get LevelGenerator for given level

        Args:
            level_type: type of level to generate

        Returns:
            configured LevelGenerator
        """
        self.logger.debug('getting generator for type {0}'.format(level_type))

        partitioner = self.get_sub_component(level_type,
                                             self.level_partitioners,
                                             'partitioner')

        room = self.get_sub_component(level_type,
                                      self.room_generators,
                                      'room')

        decorator = self.get_sub_component(level_type,
                                           self.decorators,
                                           'decorator')

        item_adder = self.get_sub_component(level_type,
                                            self.item_adders,
                                            'item adder')

        creature_adder = self.get_sub_component(level_type,
                                                self.creature_adders,
                                                'creature adder')

        portal_adder = self.get_sub_component(level_type,
                                              self.portal_adders,
                                              'portal adder')

        return LevelGenerator(self.action_factory,
                              partitioner,
                              room,
                              decorator,
                              [portal_adder],
                              item_adder,
                              creature_adder,
                              self.random_generator,
                              self.size)

    def get_sub_component(self, level_type, component_list, component_type):
        """
        Get subcomponent

        Args:
            level_type: type of level to generate
            component_list: list of subcomponents to choose from
            component_type: component type for error message
        """
        self.logger.debug('getting {0} for type {1}'.format(
                                                            component_type,
                                                            level_type))
        matches = [x for x in component_list
                   if level_type in x.level_types]

        if len(matches) > 0:
            component = self.random_generator.choice(matches)
        else:
            error_message = "No {0} for type {1} in {2}".format(
                                                            component_type,
                                                            level_type,
                                                            component_list)
            self.logger.error(error_message)
            raise RuntimeError(error_message)

        self.logger.debug('match found')
        return component

class LevelGenerator:
    """
    Class used to generate levels
    """
    def __init__(self, action_factory, partitioner, room_generator,
                 decorator, portal_adders,
                 item_adder, creature_adder,
                 random_generator, size):
        """
        Default constructor

        Args:
            action_factory: ActionFactory instance
            partitioner: LevelPartitioner to use
            room_generator: RoomGenerator to use
            decorator: LevelDecorator to use
            portal_adder: PortalAdder to use
            item_adder: ItemAdder to generate items
            creature_adder: CreatureAdder to add creatures
            random_generator: Random number generator
            size: Size of the level to create
        """
        self.logger = logging.getLogger('pyherc.generators.level.crypt.LevelGenerator') #pylint: disable=C0301
        self.item_adder = item_adder
        self.creature_adder = creature_adder
        self.random_generator = random_generator

        self.action_factory = action_factory
        self.partitioner = partitioner
        self.room_generator = room_generator
        self.decorator = decorator
        self.portal_adders = portal_adders
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

    def generate_level(self, portal):
        """
        Generate level

        Args:
            portal: Portal to link to this level
        """
        self.logger.debug('creating a new level')
        new_level = Level(self.size)

        self.logger.debug('partitioning level')
        sections = self.partitioner.partition_level(new_level, 4, 3)

        self.logger.debug('generating rooms')
        for section in sections:
            self.room_generator.generate_room(section)

        self.decorator.decorate_level(new_level)

        #for adder in self.portal_adders:
        #    adder.add_stairs(new_level, portal)

        self.creature_adder.add_creatures(new_level)

        self.item_adder.add_items(new_level)

        self.logger.debug(new_level.dump_string())

        return new_level
