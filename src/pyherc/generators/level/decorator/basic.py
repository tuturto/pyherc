#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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

class Decorator(object):
    """
    Simple decorator used to replace prototiles with real ones
    """
    def __init__(self, configuration, level):
        """
        Default constructor

        Args:
            configuration: DecoratorConfig specifying tiles to replace
        """
        super(Decorator, self).__init__()
        self.configuration = configuration
        self.level = level

    def decorate_level(self):
        """
        Decorate level
        """
        level = self.level
        tile_keys = self.configuration.ground_config.keys()
        ground_tiles = self.configuration.ground_config
        for loc_y in range(len(level.floor[0])):
            for loc_x in range(len(level.floor)):
                print loc_x, loc_y
                proto_tile = level.floor[loc_x][loc_y]
                if proto_tile in tile_keys:
                    level.floor[loc_x][loc_y] = ground_tiles[proto_tile]


class DecoratorConfig(object):
    """
    Configuration for Decorator
    """
    def __init__(self):
        """
        Default constructor
        """
        super(DecoratorConfig, self).__init__()
        self.ground_config = {}
