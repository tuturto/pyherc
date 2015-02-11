# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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

from pyherc.aspects import log_debug, log_info
from pyherc.data import new_level, Portal, add_portal, get_locations_by_tag
from pyherc.data import wall_tile


from pyherc.generators.level.partitioners.old_grid import RandomConnector
from pyherc.generators.level import (level_partitioners, room_generators,
                                     decorators, items, characters)

class LevelGeneratorFactory():
    """
    Class used to contruct different kinds of level generators
    """
    @log_debug
    def __init__(self, portal_adder_factory, configuration,
                 random_generator):
        """
        Default constructor

        :param configuration: configuration for factory
        :type configuration: LevelGeneratorFactoryConfiguration
        :param random_generator: random number generator
        :type random_generator: Random
        """
        self.logger = logging.getLogger('pyherc.generators.level.LevelGeneratorFactory')  # noqa
        self.config = configuration
        self.portal_adder_factory = portal_adder_factory
        #self.portal_adder_factory.level_generator_factory = self

        self.rng = random_generator


    @log_info
    def get_generator(self, level_type):
        """
        Get LevelGenerator for given level

        :param level_type: type of level to generate
        :type level_type: string
        :returns: configured level generator
        :rtype: LevelGenerator
        """
        partitioners = level_partitioners(self.config, level_type)
        rooms = room_generators(self.config, level_type)
        decos = decorators(self.config, level_type)
        item_adders = items(self.config, level_type)
        creature_adders = characters(self.config, level_type)

        factory = self.portal_adder_factory
        portal_adders = factory.create_portal_adders(level_type)

        #TODO: what about the None for model and level context?
        return LevelGenerator(None,
                              partitioners,
                              rooms,
                              decos,
                              portal_adders,
                              item_adders,
                              creature_adders,
                              self.rng,
                              None)

    @log_debug
    def get_sub_components(self, level_type, component_list, component_type):
        """
        Get subcomponent

        :param level_type: type of level to generate
        :type level_type: string
        :param component_list: list of subcomponents to choose from
        :type component_list: [object]
        :param component_type: component type for error message
        :type component_type: string
        :returns: components
        :rtype: [object]
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

    @log_debug
    def get_sub_component(self, level_type, component_list, component_type):
        """
        Get subcomponent

        :param level_type: type of level to generate
        :type level_type: string
        :param component_list: subcomponents to choose from
        :type component_list: [object]
        :param component_type: component type for error message
        :type component_type: string
        :returns: single component
        :rtype: object
        """
        matches = [x for x in component_list
                   if level_type in x.level_types]

        if len(matches) > 0:
            component = self.rng.choice(matches)
        else:
            error_message = "No {0} for type {1} in {2}".format(
                component_type,
                level_type,
                component_list)
            self.logger.error(error_message)
            raise RuntimeError(error_message)

        return component


class LevelGenerator():
    """
    Class used to generate levels
    """
    @log_debug
    def __init__(self, model, partitioners, room_generators,
                 decorator, portal_adders,
                 item_adder, creature_adder,
                 random_generator, level_context):
        """
        Default constructor

        :param partitioners: LevelPartitioners to use
        :param room_generators: RoomGenerators to use
        :param decorator: LevelDecorator to use
        :param portal_adder: PortalAdder to use
        :param item_adder: ItemAdder to generate items
        :param creature_adder: CreatureAdder to add creatures
        :param random_generator: Random number generator
        :param level_context: Context for level
        :param size: Size of the level to create
        """
        self.logger = logging.getLogger('pyherc.generators.level.LevelGenerator')  # noqa
        self.model = model
        self.item_adder = item_adder
        self.creature_adder = creature_adder
        self.rng = random_generator

        self.partitioners = partitioners
        self.room_generators = room_generators
        self.decorator = decorator
        self.portal_adders = portal_adders
        self.level_context = level_context

    @log_info
    def generate_level(self, portal):
        """
        Generate level

        :param portal: portal to link to this level
        :type portal: Portal
        """
        level = new_level(self.model)

        partitioner = self.rng.choice(self.partitioners)

        connector = RandomConnector(self.rng)
        sections = connector.connect_sections(partitioner(level))

        for section in sections:
            generator = self.rng.choice(self.room_generators)
            generator(section)

        for adder in self.portal_adders:
            adder.add_portal(level)

        # all this needs to be cleaned up
        if portal is not None:
            rooms = list(get_locations_by_tag(level, 'room'))
            if len(rooms) > 0:
                new_portal = Portal(icons=(portal.other_end_icon, None),
                                    level_generator_name=None)
                location = self.rng.choice(rooms)
                add_portal(level, location, new_portal, portal)
            else:
                self.logger.warn('no location found, skipping')

        for adder in self.creature_adder:
            adder.add_creatures(level)

        for adder in self.item_adder:
            adder.add_items(level)

        for decorator in self.decorator:
            decorator.decorate_level(level)

        return level
