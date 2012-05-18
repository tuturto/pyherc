#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
Module for basic decorators
"""

import logging

class Decorator(object):
    """
    Super class for level decorators
    """
    def __init__(self, configuration):
        """
        Default constructor

        :param configuration: configuration for decorator
        """
        super(Decorator, self).__init__()
        self.configuration = configuration
        self.logger = logging.getLogger('pyherc.generators.level.decorator.basic.Decorator')

    def __get_level_types(self):
        """
        Get types of levels this decorator supports

        :returns: level types
        :rtype: [string]
        """
        return self.configuration.level_types

    level_types = property(__get_level_types)

    def decorate_level(self, level):
        """
        Decorate level

        :param level: Level to decorate
        :type level: Level
        """
        pass

class DecoratorConfig(object):
    """
    Super class for decorator configuration
    """
    def __init__(self, level_types):
        """
        Default constructor

        :param level_types: level types to handle
        :type level_types: [string]
        """
        super(DecoratorConfig, self).__init__()
        self.level_types = level_types

class ReplacingDecorator(Decorator):
    """
    Simple decorator used to replace prototiles with real ones
    """
    def __init__(self, configuration):
        """
        Default constructor

        :param configuration: configuration specifying tiles to replace
        :type configuration: ReplacingDecoratorConfig
        """
        super(ReplacingDecorator, self).__init__(configuration)
        self.logger = logging.getLogger('pyherc.generators.level.decorator.basic.ReplacingDecorator')

    def decorate_level(self, level):
        """
        Decorate level

        :param level: level to decorate
        :type level: Level
        """
        floor_keys = self.configuration.ground_config.keys()
        ground_tiles = self.configuration.ground_config
        wall_keys = self.configuration.wall_config.keys()
        wall_tiles = self.configuration.wall_config

        for loc_y in range(len(level.floor[0])):
            for loc_x in range(len(level.floor)):
                proto_tile = level.floor[loc_x][loc_y]
                if proto_tile in floor_keys:
                    level.floor[loc_x][loc_y] = ground_tiles[proto_tile]

                proto_tile = level.walls[loc_x][loc_y]
                if proto_tile in wall_keys:
                    level.walls[loc_x][loc_y] = wall_tiles[proto_tile]


class ReplacingDecoratorConfig(DecoratorConfig):
    """
    Configuration for ReplacingDecorator
    """
    def __init__(self, level_types, ground_config, wall_config):
        """
        Default constructor

        :param level_types: types of level to handle
        :type level_types: [string]
        :param ground_config: configuration for ground
        :param wall_config: configuration for walls
        """
        super(ReplacingDecoratorConfig, self).__init__(level_types)
        self.ground_config = ground_config
        self.wall_config = wall_config

class WallBuilderDecorator(Decorator):
    """
    Decorator used to build walls

    This decorator will search all positions where there are walls next to empty
    space and replace tiles there with specified ones
    """
    def __init__(self, configuration):
        """
        Default constructor

        :param configuration: configuration
        :type configuration: WallBuilderDecoratorConfig
        """
        super(WallBuilderDecorator, self).__init__(configuration)
        self.logger = logging.getLogger('pyherc.generators.level.decorator.basic.WallBuilderDecorator')

    def decorate_level(self, level):
        """
        Decorate level

        :param level: level to decorate
        :type level: Level
        """
        for loc_y in range(1, len(level.floor[0]) - 1):
            for loc_x in range(1, len(level.floor) - 1):
                if level.walls[loc_x][loc_y] == self.configuration.empty_tile:
                    self.check_and_replace((loc_x - 1, loc_y), level)
                    self.check_and_replace((loc_x + 1, loc_y), level)
                    self.check_and_replace((loc_x, loc_y - 1), level)
                    self.check_and_replace((loc_x, loc_y + 1), level)
                    self.check_and_replace((loc_x - 1, loc_y - 1), level)
                    self.check_and_replace((loc_x - 1, loc_y + 1), level)
                    self.check_and_replace((loc_x + 1, loc_y - 1), level)
                    self.check_and_replace((loc_x + 1, loc_y + 1), level)

    def check_and_replace(self, location, level):
        """
        Check location and replace tile if it matches configuration

        :param location: location to check
        :type location: (integer, integer)
        :param level: level to use
        :type level: Level
        """
        loc_x = location[0]
        loc_y = location[1]
        proto_tile = level.walls[loc_x][loc_y]

        if proto_tile in self.configuration.wall_config.keys():
            tile = self.configuration.wall_config[proto_tile]
            level.walls[loc_x][loc_y] = tile

class WallBuilderDecoratorConfig(DecoratorConfig):
    """
    Configuration for WallBuilderDecorator
    """
    def __init__(self, level_types, wall_config, empty_tile):
        """
        Default constructor

        :param level_types: types of level to handle
        :type level_types: [string]
        :param wall_config: configuration for walls
        :param empty_tile: tile ID to use for empty spaces
        :type empty_tile: integer
        """
        super(WallBuilderDecoratorConfig, self).__init__(level_types)
        self.wall_config = wall_config
        self.empty_tile = empty_tile

class AggregateDecorator(Decorator):
    """
    Decorator that consists of multiple decorators
    """
    def __init__(self, configuration):
        """
        Default constructor

        :param configuration: configuration
        :type configuration: AggregateDecoratorConfig
        """
        super(AggregateDecorator, self).__init__(configuration)
        self.logger = logging.getLogger('pyherc.generators.level.decorator.basic.AggregateDecorator')

    def decorate_level(self, level):
        """
        Decorate level

        :param level: level to decorate
        :type level: Level
        """
        for decorator in self.configuration.decorators:
            decorator.decorate_level(level)

class AggregateDecoratorConfig(DecoratorConfig):
    """
    Configuration for AggregateDecorator
    """
    def __init__(self, level_types, decorators):
        """
        Default constructor

        :param level_types: types of levels to handle
        :type level_types: [string]
        :decorators: decorators to group
        :type decorators: [Decorator]
        """
        super(AggregateDecoratorConfig, self).__init__(level_types)
        self.decorators = decorators
