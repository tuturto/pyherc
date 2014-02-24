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
module for configuring upper crypt
"""
from pyherc.generators.level.partitioners import GridPartitioner
from pyherc.generators.level.room import SquareRoomGenerator, PillarRoomGenerator

from pyherc.generators.level.decorator import ReplacingDecorator
from pyherc.generators.level.decorator import ReplacingDecoratorConfig
from pyherc.generators.level.decorator import WallBuilderDecorator
from pyherc.generators.level.decorator import WallBuilderDecoratorConfig
from pyherc.generators.level.decorator import DirectionalWallDecoratorConfig
from pyherc.generators.level.decorator import DirectionalWallDecorator
from pyherc.generators.level.decorator import FloorBuilderDecoratorConfig
from pyherc.generators.level.decorator import FloorBuilderDecorator
from pyherc.generators.level.decorator import AggregateDecorator
from pyherc.generators.level.decorator import AggregateDecoratorConfig

from pyherc.generators.level.items import ItemAdderConfiguration, ItemAdder
from pyherc.generators.level.creatures import CreatureAdderConfiguration
from pyherc.generators.level.creatures import CreatureAdder

from pyherc.generators.level.portals import PortalAdderConfiguration

from herculeum.ai import FlockingHerbivore
from pyherc.generators import CreatureConfiguration
from pyherc.data.effects import EffectHandle

from pyherc.config.dsl import LevelConfiguration, LevelContext

def init_level(rng, item_generator, creature_generator, level_size, context):
    """
    Initialise upper crypt levels

    :returns: level configuration
    :rtype: LevelConfiguration
    """
    surface_manager = context.surface_manager

    floor_natural = 'natural floor'
    floor_rock = surface_manager.add_icon('floor_rock', ':rock_floor.png', '.')
    floor_constructed = 'constructed floor'
    floor_tiled = surface_manager.add_icon('floor_tiled', ':tiled_floor.png', '.')

    wall_empty = surface_manager.add_icon('empty wall', ':transparent.png', None)
    wall_natural = 'natural wall'
    wall_constructed = 'constructed wall'
    wall_ground = surface_manager.add_icon('wall_ground', ':ground_wall.png', ' ')
    wall_rock = surface_manager.add_icon('wall_rock', ':rock_wall.png', '#')
    pillar = surface_manager.add_icon('pillar', ':pillar.png', '#')

    stairs_down = surface_manager.add_icon('stairs_down', ':stairs_down.png', '>')
    stairs_up = surface_manager.add_icon('stairs_up', ':stairs_up.png', '<')

    wall = surface_manager.add_icon('crypt_wall', ':crypt_wall.png', '#')
    wall_15 = surface_manager.add_icon('crypt_wall_15', ':crypt_wall_15.png', '#')
    wall_57 = surface_manager.add_icon('crypt_wall_57', ':crypt_wall_57.png', '#')
    wall_35 = surface_manager.add_icon('crypt_wall_35', ':crypt_wall_35.png', '#')
    wall_37 = surface_manager.add_icon('crypt_wall_37', ':crypt_wall_37.png', '#')
    wall_17 = surface_manager.add_icon('crypt_wall_17', ':crypt_wall_17.png', '#')
    wall_13 = surface_manager.add_icon('crypt_wall_13', ':crypt_wall_13.png', '#')
    wall_135 = surface_manager.add_icon('crypt_wall_135', ':crypt_wall_135.png', '#')
    wall_357 = surface_manager.add_icon('crypt_wall_357', ':crypt_wall_357.png', '#')
    wall_1357 = surface_manager.add_icon('crypt_wall_1357', ':crypt_wall_1357.png', '#')
    wall_137 = surface_manager.add_icon('crypt_wall_137', ':crypt_wall_137.png', '#')
    wall_157 = surface_manager.add_icon('crypt_wall_157', ':crypt_wall_157.png', '#')

    room_generators = [SquareRoomGenerator(floor_natural,
                                           wall_empty,
                                           floor_natural,
                                           ['upper crypt']),
                       SquareRoomGenerator(floor_constructed,
                                           wall_empty,
                                           floor_natural,
                                           ['upper crypt']),
                       PillarRoomGenerator(floor_tile = floor_constructed,
                                           corridor_tile = floor_natural,
                                           empty_tile = wall_empty,
                                           pillar_tile = wall,
                                           level_types = ['upper crypt'])
                                           ]
    level_partitioners = [GridPartitioner(['upper crypt'],
                                          4,
                                          2,
                                          rng)]

    replacer_config = ReplacingDecoratorConfig(['upper crypt'],
                                    {floor_natural: floor_rock,
                                    floor_constructed: floor_tiled},
                                    {wall_natural: wall_ground,
                                    wall_constructed: wall_rock})
    replacer = ReplacingDecorator(replacer_config)

    wallbuilder_config = WallBuilderDecoratorConfig(['upper crypt'],
                                        {wall_natural: wall_constructed},
                                        wall_empty)
    wallbuilder = WallBuilderDecorator(wallbuilder_config)

    wall_direction_config = DirectionalWallDecoratorConfig(['upper crypt'],
                                                   east_west = wall_37,
                                                   east_north = wall_13,
                                                   east_south = wall_35,
                                                   west_north = wall_17,
                                                   west_south = wall_57,
                                                   north_south = wall_15,
                                                   east_west_north = wall_137,
                                                   east_west_south = wall_357,
                                                   east_north_south = wall_135,
                                                   west_north_south = wall_157,
                                                   four_way = wall_1357,
                                                   wall = wall_constructed)

    wall_direction_builder = DirectionalWallDecorator(wall_direction_config)

    floor = surface_manager.add_icon('crypt_floor', ':crypt_floor.png', ' ')
    floor1 = surface_manager.add_icon('crypt_floor_1', ':crypt_floor_1.png', ' ')
    floor3 = surface_manager.add_icon('crypt_floor_3', ':crypt_floor_3.png', ' ')
    floor5 = surface_manager.add_icon('crypt_floor_5', ':crypt_floor_5.png', ' ')
    floor7 = surface_manager.add_icon('crypt_floor_7', ':crypt_floor_7.png', ' ')
    floor13 = surface_manager.add_icon('crypt_floor_13', ':crypt_floor_13.png', ' ')
    floor15 = surface_manager.add_icon('crypt_floor_15', ':crypt_floor_15.png', ' ')
    floor17 = surface_manager.add_icon('crypt_floor_17', ':crypt_floor_17.png', ' ')
    floor35 = surface_manager.add_icon('crypt_floor_35', ':crypt_floor_35.png', ' ')
    floor37 = surface_manager.add_icon('crypt_floor_37', ':crypt_floor_37.png', ' ')
    floor57 = surface_manager.add_icon('crypt_floor_57', ':crypt_floor_57.png', ' ')
    floor135 = surface_manager.add_icon('crypt_floor_135', ':crypt_floor_135.png', ' ')
    floor137 = surface_manager.add_icon('crypt_floor_137', ':crypt_floor_137.png', ' ')
    floor157 = surface_manager.add_icon('crypt_floor_157', ':crypt_floor_157.png', ' ')
    floor357 = surface_manager.add_icon('crypt_floor_357', ':crypt_floor_357.png', ' ')
    floor1357 = surface_manager.add_icon('crypt_floor_1357', ':crypt_floor_1357.png', ' ')

    floor_config = FloorBuilderDecoratorConfig([],
                                               single = floor,
                                               north = floor1,
                                               east = floor3,
                                               south = floor5,
                                               west = floor7,
                                               north_east = floor13,
                                               north_south = floor15,
                                               north_west = floor17,
                                               east_south = floor35,
                                               east_west = floor37,
                                               south_west = floor57,
                                               north_east_south = floor135,
                                               north_east_west = floor137,
                                               north_south_west = floor157,
                                               east_south_west = floor357,
                                               fourway = floor1357,
                                               floor = floor_natural)
    floor_builder = FloorBuilderDecorator(floor_config)

    aggregate_decorator_config = AggregateDecoratorConfig(['upper crypt'],
                                                          [wallbuilder,
                                                           wall_direction_builder,
                                                           floor_builder,
                                                           replacer])

    decorators = [AggregateDecorator(aggregate_decorator_config)]

    item_adder_config = ItemAdderConfiguration(['upper crypt'])
    item_adder_config.add_item(min_amount = 2,
                               max_amount = 4,
                               type = 'weapon',
                               location = 'room')
    item_adder_config.add_item(min_amount = 2,
                               max_amount = 4,
                               type = 'potion',
                               location = 'room')
    item_adder_config.add_item(min_amount = 0,
                               max_amount = 5,
                               type = 'food',
                               location = 'room')
    item_adder_config.add_item(min_amount = 0,
                               max_amount = 1,
                               type = 'tome',
                               location = 'room')
    item_adders = [ItemAdder(item_generator,
                            item_adder_config,
                            rng)]

    creature_adder_config = CreatureAdderConfiguration(['upper crypt'])

    creature_adder_config.add_creature(min_amount = 4,
                                       max_amount = 8,
                                       name = 'spider')

    creature_adders = [CreatureAdder(creature_generator,
                                    creature_adder_config,
                                    rng)]

    portal_adder_configurations = [PortalAdderConfiguration(
                                        icons = (stairs_down,
                                                 stairs_up),
                                        level_type = 'upper catacombs',
                                        location_type = 'room',
                                        chance = 10,
                                        new_level = 'upper crypt',
                                        unique = True)]

    level_context = LevelContext(size = level_size,
                                 floor_type = None,
                                 wall_type = wall_natural,
                                 empty_floor = 0,
                                 empty_wall = wall_empty,
                                 level_types = ['upper crypt',
                                                'lower crypt'])

    config = (LevelConfiguration()
                    .with_rooms(room_generators)
                    .with_partitioners(level_partitioners)
                    .with_decorators(decorators)
                    .with_items(item_adders)
                    .with_creatures(creature_adders)
                    .with_portals(portal_adder_configurations)
                    .with_contexts([level_context])
                    .build())
    return config

def init_creatures(context):
    """
    Initialise creatures

    :returns: list of creature configurations
    :rtype: [CreatureConfiguration]
    """
    config = []
    surface_manager = context.surface_manager

    config.append(CreatureConfiguration(name = 'spider',
                                        body = 6,
                                        finesse = 12,
                                        mind = 8,
                                        hp = 6,
                                        speed = 1,
                                        icons = surface_manager.add_icon('spider', ':masked-spider.png', 's', ['white', 'dim']),
                                        attack = 4,
                                        ai = FlockingHerbivore,
                                        effect_handles = [EffectHandle(
                                                    trigger = 'on attack hit',
                                                    effect = 'minor poison',
                                                    parameters = None,
                                                    charges = 100)]))

    return config
