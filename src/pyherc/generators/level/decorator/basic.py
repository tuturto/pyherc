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
Module for basic decorators
"""
from pyherc.data import (floor_tile, wall_tile, ornamentation, get_tiles,
                         get_tile)


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

    def __call__(self, level):
        """
        decorate level
        """
        self.decorate_level(level)

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
        wall_tiles = []
        wall_tiles.append(self.configuration.wall)
        wall_tiles.extend(self.tiles.values())

        pillar = self.check_pillar(level, location)
        if pillar:
            return pillar

        if wall_tile(level, (loc_x, loc_y - 1)) in self.configuration.tiles:
            if not (is_wall(level, (loc_x - 1, loc_y - 1), wall_tiles)
                    and is_wall(level, (loc_x + 1, loc_y - 1), wall_tiles)
                    and is_wall(level, (loc_x - 1, loc_y), wall_tiles)
                    and is_wall(level, (loc_x + 1, loc_y), wall_tiles)):
                directions.append('1')
        if wall_tile(level, (loc_x + 1, loc_y)) in self.configuration.tiles:
            if not (is_wall(level, (loc_x + 1, loc_y - 1), wall_tiles)
                    and is_wall(level, (loc_x + 1, loc_y + 1), wall_tiles)
                    and is_wall(level, (loc_x, loc_y - 1), wall_tiles)
                    and is_wall(level, (loc_x, loc_y + 1), wall_tiles)):
                directions.append('3')
        if wall_tile(level, (loc_x, loc_y + 1)) in self.configuration.tiles:
            if not (is_wall(level, (loc_x - 1, loc_y + 1), wall_tiles)
                    and is_wall(level, (loc_x + 1, loc_y + 1), wall_tiles)
                    and is_wall(level, (loc_x - 1, loc_y), wall_tiles)
                    and is_wall(level, (loc_x + 1, loc_y), wall_tiles)):
                directions.append('5')
        if wall_tile(level, (loc_x - 1, loc_y)) in self.configuration.tiles:
            if not (is_wall(level, (loc_x - 1, loc_y - 1), wall_tiles)
                    and is_wall(level, (loc_x - 1, loc_y + 1), wall_tiles)
                    and is_wall(level, (loc_x, loc_y - 1), wall_tiles)
                    and is_wall(level, (loc_x, loc_y + 1), wall_tiles)):
                directions.append('7')

        key = ''.join(directions)

        if key in self.tiles:
            return self.tiles[''.join(directions)]
        else:
            return self.configuration.four_way

    def check_pillar(self, level, location):
        "check for possible pillar"
        tiles = self.configuration.tiles
        x_loc, y_loc = location
        
        if (wall_tile(level, (x_loc - 1, y_loc)) not in tiles
                and wall_tile(level, (x_loc + 1, y_loc)) not in tiles
                and wall_tile(level, (x_loc, y_loc - 1)) not in tiles
                and wall_tile(level, (x_loc, y_loc + 1)) not in tiles):

            return self.configuration.wall

        return None

def is_wall(level, location, wall_tiles):
    "check if given location is considered as a wall"
    return (get_tile(level, location) is None 
            or wall_tile(level, location) in wall_tiles)

class FloorBuilderDecoratorConfig(DecoratorConfig):
    """
    Configuration for FloorBuilderDecorator

    .. versionadded:: 0.10
    """
    def __init__(self, level_types,
                 single, north, east, south, west, north_east, north_south,
                 north_west, east_south, east_west, south_west,
                 north_east_south, north_east_west, north_south_west,
                 east_south_west, fourway, floor,
                 nook_west, nook_east):
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
        self.nook_west = nook_west
        self.nook_east = nook_east

        self.tiles = [single, north, east, south, west, north_east,
                      north_south, north_west, east_south, east_west,
                      south_west, north_east_south, north_east_west,
                      north_south_west, east_south_west, fourway, floor,
                      nook_west, nook_east]


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

        self.nook_west = configuration.nook_west
        self.nook_east = configuration.nook_east

        self.second_pass = []

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

        for location in self.second_pass:
            if get_tile(level, location):
                floor_tile(level, location,
                           self.check_nook(level, location))
                

    def check_nook(self, level, location):
        loc_x, loc_y = location

        if (floor_tile(level, (loc_x, loc_y - 1)) in [self.tiles['15'],
                                                      self.tiles['35']]
            and floor_tile(level, (loc_x + 1, loc_y)) in self.configuration.tiles
            and floor_tile(level, (loc_x - 1, loc_y)) in [self.tiles['37'],
                                                          self.tiles['35']]):
            return self.nook_west

        if (floor_tile(level, (loc_x, loc_y - 1)) in [self.tiles['15'],
                                                      self.tiles['57']]
            and floor_tile(level, (loc_x - 1, loc_y)) in self.configuration.tiles
            and floor_tile(level, (loc_x + 1, loc_y)) in [self.tiles['37'],
                                                          self.tiles['57']]):
            return self.nook_east

        return self.tiles['1357']

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

        if (floor_tile(level, (loc_x - 1, loc_y - 1)) not in self.configuration.tiles
            and floor_tile(level, (loc_x, loc_y - 1)) in self.configuration.tiles
            and floor_tile(level, (loc_x + 1, loc_y)) in self.configuration.tiles
            and floor_tile(level, (loc_x - 1, loc_y)) in self.configuration.tiles):
            self.second_pass.append(location)
            return self.tiles['']

        if (floor_tile(level, (loc_x + 1, loc_y - 1)) not in self.configuration.tiles
            and floor_tile(level, (loc_x, loc_y - 1)) in self.configuration.tiles
            and floor_tile(level, (loc_x - 1, loc_y)) in self.configuration.tiles
            and floor_tile(level, (loc_x + 1, loc_y)) in self.configuration.tiles):
            self.second_pass.append(location)
            return self.tiles['']

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
                    if (self.configuration.top_only == False
                        or floor_tile(level, (location[0], location[1] + 1))):
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
    def __init__(self, level_types, wall_tile, ornamentation, rng, rate,
                 top_only = True):
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
        self.top_only = top_only
        self.rng = rng
        self.rate = rate
