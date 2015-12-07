# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Classs needed for generating levels
"""

import logging

from pyherc.aspects import log_debug, log_info
from pyherc.data import new_level, Portal, add_portal, get_locations_by_tag
from pyherc.data import wall_tile


from pyherc.generators.level.partitioners.old_grid import RandomConnector
from pyherc.generators.level import (level_partitioners, room_generators,
                                     decorators, items, characters, description)
from pyherc.generators.level.new_generator import new_level_generator

class LevelGeneratorFactory():
    """
    Class used to contruct different kinds of level generators
    """
    @log_debug
    def __init__(self, portal_adder_factory, trap_generator, configuration,
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
        self.trap_generator = trap_generator
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
        return new_level_generator(None,
                                   partitioners,
                                   rooms,
                                   decos,
                                   portal_adders,
                                   item_adders,
                                   creature_adders,
                                   self.trap_generator,
                                   self.rng,
                                   level_type,
                                   description(self.config, level_type))


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
