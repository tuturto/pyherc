# -*- coding: utf-8 -*-

#   Copyright 2010-2015 Tuukka Turto
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
from herculeum.ai import FlockingHerbivore
from pyherc.config.dsl import LevelConfiguration, LevelContext
from pyherc.data.effects import EffectHandle
from pyherc.data.traps import PitTrap
from pyherc.generators import creature_config
from pyherc.generators.level.creatures import (CreatureAdder,
                                               CreatureAdderConfiguration)
from pyherc.generators.level.decorator import (DirectionalWallDecorator,
                                               DirectionalWallDecoratorConfig,
                                               FloorBuilderDecorator,
                                               FloorBuilderDecoratorConfig,
                                               SurroundingDecorator,
                                               SurroundingDecoratorConfig,
                                               WallBuilderDecorator,
                                               WallBuilderDecoratorConfig,
                                               WallOrnamentDecorator,
                                               WallOrnamentDecoratorConfig)
from pyherc.generators.level import ItemAdder, ItemAdderConfiguration, new_level
from pyherc.generators.level.partitioners import grid_partitioning
from pyherc.generators.level import PortalAdderConfiguration
from pyherc.generators.level.room import (PillarRoomGenerator,
                                          SquareRoomGenerator)
from herculeum.config.room_generators import (circular_pitroom, square_pitroom,
                                              square_room)
from herculeum.config.floor_builders import floor_builder, pit_builder


def init_level(rng, item_generator, creature_generator, level_size, context):
    """
    Initialise upper crypt levels

    :returns: level configuration
    :rtype: LevelConfiguration
    """
    surface_manager = context.surface_manager

    wall_empty = None
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

    room_generators = [PillarRoomGenerator(floor_tile = 'ground_wood4',
                                           corridor_tile = 'ground_tile4',
                                           empty_tile = wall_empty,
                                           pillar_tile = wall,
                                           level_types = ['upper crypt']),
                       PillarRoomGenerator(floor_tile = 'ground_tile4',
                                           corridor_tile = 'ground_tile4',
                                           empty_tile = wall_empty,
                                           pillar_tile = wall,
                                           level_types = ['upper crypt']),
                                        ]

    room_generators = [circular_pitroom('ground_tile4', 
                                        'ground_tile4', 
                                        'brick_pit_07', 
                                        rng),
                       circular_pitroom('ground_wood4',
                                        'ground_tile4',
                                        'brick_pit_07',
                                        rng),
                       square_pitroom('ground_tile4', 
                                      'ground_tile4', 
                                      'brick_pit_07', 
                                      rng),
                       square_pitroom('ground_wood4',
                                      'ground_tile4',
                                      'brick_pit_07',
                                      rng),
                       square_room('ground_tile4',
                                   'ground_tile4',
                                   rng),
                       square_room('ground_wood4',
                                   'ground_tile4',
                                   rng)]

    level_partitioners = [grid_partitioning((15, 15), 4, 6, rng)]

    surrounder_config = SurroundingDecoratorConfig(['upper crypt'],
                                                   wall_constructed)
    surrounder = SurroundingDecorator(surrounder_config)

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

    torches_tile_f0 = surface_manager.add_icon('crypt_torches_f0', ':wall_torches_f0.png', '¤')
    torches_tile_f1 = surface_manager.add_icon('crypt_torches_f1', ':wall_torches_f1.png', '¤')
    torch_tile_f0 = surface_manager.add_icon('crypt_torch_f0', ':wall_torch_f0.png', '¤')
    torch_tile_f1 = surface_manager.add_icon('crypt_torch_f1', ':wall_torch_f1.png', '¤')

    torch_ornamenter_config = WallOrnamentDecoratorConfig(
                                                ['upper crypt'],
                                                wall_tile = wall_37,
                                                ornamentation = [(torch_tile_f0,
                                                                  torch_tile_f1),
                                                                 (torches_tile_f0,
                                                                  torches_tile_f1)],
                                                rng = rng,
                                                rate = 13)
    torch_ornamenter = WallOrnamentDecorator(torch_ornamenter_config)

    decorators = [surrounder,
                  wall_direction_builder,
                  floor_builder('ground_tile4'),
                  floor_builder('ground_wood4'),
                  pit_builder('brick_pit'),
                  torch_ornamenter]

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
                                        level_type = 'lower catacombs',
                                        location_type = 'room',
                                        chance = 10,
                                        new_level = 'upper crypt',
                                        unique = True)]

    return [new_level('upper crypt', room_generators, level_partitioners,
                      decorators, item_adders, creature_adders,
                      portal_adder_configurations)]


def init_creatures(context):
    """
    Initialise creatures

    :returns: list of creature configurations
    :rtype: [CreatureConfiguration]
    """
    config = []
    surface_manager = context.surface_manager

    spider_f0 = surface_manager.add_icon('spider_f0', ':masked-spider_f0.png', 's', ['white', 'dim'])
    spider_f1 = surface_manager.add_icon('spider_f1', ':masked-spider_f1.png', 's', ['white', 'dim'])
    config.append(creature_config(name = 'spider',
                                  body = 6,
                                  finesse = 12,
                                  mind = 8,
                                  hp = 6,
                                  speed = 1,
                                  icons = (spider_f0, spider_f1),
                                  attack = 4,
                                  ai = FlockingHerbivore,
                                  effect_handles = [EffectHandle(
                                      trigger = 'on attack hit',
                                      effect = 'minor poison',
                                      parameters = None,
                                      charges = 100)]))

    return config
