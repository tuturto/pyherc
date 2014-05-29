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
Module for basic decorators
"""
from pyherc.data import floor_tile, wall_tile, ornamentation, get_tiles

class Decorator():
    """
    Super class for level decorators
    """
    def __init__(self, configuration):
        """
        Default constructor

        :param configuration: configuration for decorator
        """
        super().__init__()
        self.configuration = configuration

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


class DecoratorConfig():
    """
    Super class for decorator configuration
    """
    def __init__(self, level_types):
        """
        Default constructor

        :param level_types: level types to handle
        :type level_types: [string]
        """
        super().__init__()
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
        super().__init__(configuration)

    def decorate_level(self, level):
        """
        Decorate level

        :param level: level to decorate
        :type level: Level
        """
        ground_tiles = self.configuration.ground_config
        wall_tiles = self.configuration.wall_config

        for location, tile in get_tiles(level):
            proto_tile = tile['\ufdd0:floor']
            if proto_tile in ground_tiles:
                tile['\ufdd0:floor'] = ground_tiles[proto_tile]

            proto_tile = tile['\ufdd0:wall']
            if proto_tile in wall_tiles:
                tile['\ufdd0:wall'] = wall_tiles[proto_tile]

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
        super().__init__(level_types)
        self.ground_config = ground_config
        self.wall_config = wall_config


class WallBuilderDecorator(Decorator):
    """
    Decorator used to build walls

    This decorator will search all positions where there are walls next to
    empty space and replace tiles there with specified ones
    """
    def __init__(self, configuration):
        """
        Default constructor

        :param configuration: configuration
        :type configuration: WallBuilderDecoratorConfig
        """
        super().__init__(configuration)

    def decorate_level(self, level):
        """
        Decorate level

        :param level: level to decorate
        :type level: Level
        """
        empty_tile = self.configuration.empty_tile

        for loc, tile in list(get_tiles(level)):
            if tile['\ufdd0:wall'] == empty_tile:
                self.check_and_replace((loc[0] - 1, loc[1]), level)
                self.check_and_replace((loc[0] + 1, loc[1]), level)
                self.check_and_replace((loc[0], loc[1] - 1), level)
                self.check_and_replace((loc[0], loc[1] + 1), level)
                self.check_and_replace((loc[0] - 1, loc[1] - 1), level)
                self.check_and_replace((loc[0] - 1, loc[1] + 1), level)
                self.check_and_replace((loc[0] + 1, loc[1] - 1), level)
                self.check_and_replace((loc[0] + 1, loc[1] + 1), level)

    def check_and_replace(self, location, level):
        """
        Check location and replace tile if it matches configuration

        :param location: location to check
        :type location: (integer, integer)
        :param level: level to use
        :type level: Level
        """
        proto_tile = wall_tile(level, location)

        if proto_tile in self.configuration.wall_config:
            tile = self.configuration.wall_config[proto_tile]
            wall_tile(level, location, tile)


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
        super().__init__(level_types)
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
        super().__init__(configuration)

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
        super().__init__(level_types)
        self.decorators = decorators


class DirectionalWallDecoratorConfig(DecoratorConfig):
    """
    Configuration for DirectionalWallDecorator

    .. versionadded:: 0.10
    """
    def __init__(self, level_types, east_west, east_north, east_south,
                 west_north, west_south, north_south,
                 east_west_north, east_west_south,
                 east_north_south, west_north_south,
                 four_way, wall):
        """
        Default constructor
        """
        super().__init__(level_types)
        self.east_west = east_west
        self.east_north = east_north
        self.east_south = east_south
        self.west_north = west_north
        self.west_south = west_south
        self.north_south = north_south

        self.east_west_north = east_west_north
        self.east_west_south = east_west_south
        self.east_north_south = east_north_south
        self.west_north_south = west_north_south
        self.four_way = four_way

        self.wall = wall

        self.tiles = [east_west, east_north, east_south,
                      west_north, west_south, north_south,
                      east_west_north, east_west_south,
                      east_north_south, west_north_south,
                      four_way, wall]


class DirectionalWallDecorator(Decorator):
    """
    Decorator to build directional walls

    .. versionadded:: 0.10
    """
    def __init__(self, configuration):
        """
        Default constructor

        :param configuration: configuration
        :type configuration: DirectionalWallDecoratorConfig
        """
        super().__init__(configuration)

        self.tiles = {'1': configuration.north_south,
                      '13': configuration.east_north,
                      '15': configuration.north_south,
                      '17': configuration.west_north,
                      '135': configuration.east_north_south,
                      '137': configuration.east_west_north,
                      '157': configuration.west_north_south,
                      '1357': configuration.four_way,
                      '3': configuration.east_west,
                      '35': configuration.east_south,
                      '37': configuration.east_west,
                      '357': configuration.east_west_south,
                      '5': configuration.north_south,
                      '57': configuration.west_south,
                      '7': configuration.east_west}

    def decorate_level(self, level):
        """
        Decorate level

        :param level: level to decorate
        :type level: Level
        """
        wall = self.configuration.wall

        for location, tile in get_tiles(level):
            if tile['\ufdd0:wall'] == wall:
                tile['\ufdd0:wall'] = self.get_wall_tile(level, location)

    def get_wall_tile(self, level, location):
        """
        Calculate correct wall tile

        :param level: level to decorate
        :type level: Level
        :param location: location in level
        :type location: (int, int)
        :rtype: int
        """

        directions = []
        loc_x, loc_y = location

        if wall_tile(level, (loc_x, loc_y - 1)) in self.configuration.tiles:
            directions.append('1')
        if wall_tile(level, (loc_x + 1, loc_y)) in self.configuration.tiles:
            directions.append('3')
        if wall_tile(level, (loc_x, loc_y + 1)) in self.configuration.tiles:
            directions.append('5')
        if wall_tile(level, (loc_x - 1, loc_y)) in self.configuration.tiles:
            directions.append('7')

        key = ''.join(directions)

        if key in self.tiles:
            return self.tiles[''.join(directions)]
        else:
            return self.configuration.east_west


class FloorBuilderDecoratorConfig(DecoratorConfig):
    """
    Configuration for FloorBuilderDecorator

    .. versionadded:: 0.10
    """
    def __init__(self, level_types,
                 single, north, east, south, west, north_east, north_south,
                 north_west, east_south, east_west, south_west,
                 north_east_south, north_east_west, north_south_west,
                 east_south_west, fourway, floor):
        """
        Default constructor
        """
        super().__init__(level_types)

        self.single = single
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.north_east = north_east
        self.north_south = north_south
        self.north_west = north_west
        self.east_south = east_south
        self.east_west = east_west
        self.south_west = south_west
        self.north_east_south = north_east_south
        self.north_east_west = north_east_west
        self.east_south_west = east_south_west
        self.north_south_west = north_south_west
        self.fourway = fourway
        self.floor = floor

        self.tiles = [single, north, east, south, west, north_east,
                      north_south, north_west, east_south, east_west,
                      south_west, north_east_south, north_east_west,
                      north_south_west, east_south_west, fourway, floor]


class FloorBuilderDecorator(Decorator):
    """
    Decorator to build floors

    .. versionadded:: 0.10
    """
    def __init__(self, configuration):
        """
        Default constructor

        :param configuration: configuration
        :type configuration: FloorBuilderDecoratorConfig
        """
        super().__init__(configuration)

        self.tiles = {'': configuration.single,
                      '1': configuration.north,
                      '3': configuration.east,
                      '5': configuration.south,
                      '7': configuration.west,
                      '13': configuration.north_east,
                      '15': configuration.north_south,
                      '17': configuration.north_west,
                      '35': configuration.east_south,
                      '37': configuration.east_west,
                      '57': configuration.south_west,
                      '135': configuration.north_east_south,
                      '137': configuration.north_east_west,
                      '157': configuration.north_south_west,
                      '357': configuration.east_south_west,
                      '1357': configuration.fourway}

    def decorate_level(self, level):
        """
        Decorate level

        :param level: level to decorate
        :type level: Level
        """
        floor = self.configuration.floor
        for location, tile in get_tiles(level):
            if tile['\ufdd0:floor'] == floor:
                floor_tile(level, location,
                           self.get_floor_tile(level, location))

    def get_floor_tile(self, level, location):
        """
        Calculate correct floor tile

        :param level: level to decorate
        :type level: Level
        :returns: new floor tile
        :rtype: int
        """

        loc_x, loc_y = location
        directions = []
        if floor_tile(level, (loc_x, loc_y - 1)) in self.configuration.tiles:
            directions.append('1')
        if floor_tile(level, (loc_x + 1, loc_y)) in self.configuration.tiles:
            directions.append('3')
        if floor_tile(level, (loc_x, loc_y + 1)) in self.configuration.tiles:
            directions.append('5')
        if floor_tile(level, (loc_x - 1, loc_y)) in self.configuration.tiles:
            directions.append('7')

        key = ''.join(directions)

        if key in self.tiles:
            return self.tiles[''.join(directions)]
        else:
            return self.configuration.east_west


class WallOrnamentDecorator(Decorator):
    """
    Decorator to place ornaments of walls

    .. versionadded:: 0.10
    """
    def __init__(self, configuration):
        """
        Default constructor

        :param configuration: configuration to use
        :type configuration: WallOrnamentDecoratorConfig
        """
        super().__init__(configuration)

    def decorate_level(self, level):
        """
        Decorate level

        :param level: level to decorate
        :type level: Level
        """
        wall = self.configuration.wall_tile
        rate = self.configuration.rate

        for location, tile in get_tiles(level):
            if tile['\ufdd0:wall'] == wall:
                if self.configuration.rng.randint(0, 100) < rate:
                    if floor_tile(level, (location[0], location[1] + 1)):
                        self._randomize_ornament(level, location)

    def _randomize_ornament(self, level, location):
        """
        Set random ornament to given location

        :param level: level to ornament
        :type level: Level
        """
        rng = self.configuration.rng
        ornaments = self.configuration.ornamentation

        ornamentation(level, location, rng.choice(ornaments))


class WallOrnamentDecoratorConfig(DecoratorConfig):
    """
    Configuration for WallOrnamentDecorator

    .. versionadded:: 0.10
    """
    def __init__(self, level_types, wall_tile, ornamentation, rng, rate):
        """
        Default constructor

        :param level_types: types of levels to decorate
        :type level_types: [string]
        :param wall_tile: wall to decorate
        :type wall_tile: string
        :param ornamentation: ornamentation to place
        :type ornamentation: string
        :param rng: random number generator
        :type rng: Random
        :param rate: rate of ornamentation
        :type rate: integer 0 <= rate <= 100
        """
        super().__init__(level_types)
        self.wall_tile = wall_tile
        self.ornamentation = ornamentation
        self.rng = rng
        self.rate = rate
