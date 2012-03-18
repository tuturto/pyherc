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
from pyherc.data import Level, Portal
from pyherc.aspects import Logged

class LevelGeneratorFactory:
    """
    Class used to contruct different kinds of level generators
    """

    logged = Logged()

    @logged
    def __init__(self, action_factory, portal_adder_factory, configuration,
                 random_generator):
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
        self.portal_adder_configurations = configuration.portal_adder_configurations
        self.portal_adder_factory = portal_adder_factory
        self.portal_adder_factory.level_generator_factory = self
        self.item_adders = configuration.item_adders
        self.creature_adders = configuration.creature_adders
        self.size = configuration.size
        self.random_generator = random_generator

    @logged
    def get_generator(self, level_type):
        """
        Get LevelGenerator for given level

        Args:
            level_type: type of level to generate

        Returns:
            configured LevelGenerator
        """
        partitioner = self.get_sub_component(level_type,
                                             self.level_partitioners,
                                             'partitioner')

        rooms = self.get_sub_components(level_type,
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

        portal_adders = self.portal_adder_factory.create_portal_adders(level_type)

        return LevelGenerator(self.action_factory,
                              partitioner,
                              rooms,
                              decorator,
                              portal_adders,
                              item_adder,
                              creature_adder,
                              self.random_generator,
                              self.size)

    @logged
    def get_sub_components(self, level_type, component_list, component_type):
        """
        Get subcomponent

        Args:
            level_type: type of level to generate
            component_list: list of subcomponents to choose from
            component_type: component type for error message

        Returns:
            List of components
        """
        components = [x for x in component_list
                      if level_type in x.level_types]

        if len(components) == 0:
            error_message = "No {0} for type {1} in {2}".format(
                                                            component_type,
                                                            level_type,
                                                            component_list)
            self.logger.error(error_message)
            raise RuntimeError(error_message)

        return components

    @logged
    def get_sub_component(self, level_type, component_list, component_type):
        """
        Get subcomponent

        Args:
            level_type: type of level to generate
            component_list: list of subcomponents to choose from
            component_type: component type for error message

        Returns:
            Single component
        """
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

        return component

class LevelGenerator:
    """
    Class used to generate levels
    """
    logged = Logged()

    @logged
    def __init__(self, action_factory, partitioner, room_generators,
                 decorator, portal_adders,
                 item_adder, creature_adder,
                 random_generator, size):
        """
        Default constructor

        Args:
            action_factory: ActionFactory instance
            partitioner: LevelPartitioner to use
            room_generators: RoomGenerators to use
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
        self.room_generators = room_generators
        self.decorator = decorator
        self.portal_adders = portal_adders
        self.size = size

    def __getstate__(self):
        """
        Override __getstate__ in order to get pickling work
        """
        data = dict(self.__dict__)
        del data['logger']
        return data

    def __setstate__(self, data):
        """
        Override __setstate__ in order to get pickling work
        """
        self.__dict__.update(data)
        self.logger = logging.getLogger('pyherc.generators.level.crypt.LevelGenerator') #pylint: disable=C0301

    @logged
    def generate_level(self, portal):
        """
        Generate level

        Args:
            portal: Portal to link to this level
        """
        #TODO: configurable
        new_level = Level(self.size, -2, -101)

        sections = self.partitioner.partition_level(new_level)

        for section in sections:
            generator = self.random_generator.choice(self.room_generators)
            generator.generate_room(section)

        self.decorator.decorate_level(new_level)

        for adder in self.portal_adders:
            adder.add_portal(new_level)

        # all this needs to be cleaned up
        if portal != None:
            rooms = new_level.get_locations_by_type('room')
            if len(rooms) > 0:
                new_portal = Portal(icons = (portal.other_end_icon, None),
                                    level_generator = None)
                location = self.random_generator.choice(rooms)
                new_level.add_portal(new_portal, location, portal)
            else:
                self.logger.warn('no location found, skipping')


        self.creature_adder.add_creatures(new_level)

        self.item_adder.add_items(new_level)

        self.logger.debug(new_level.dump_string())

        return new_level
