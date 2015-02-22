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
module for configuring first gate
"""
import hy

from herculeum.ai.fungus import FungusAI, GreatFungusAI
from herculeum.config.room_generators import (square_room, circular_room,
                                              square_graveyard,
                                              circular_graveyard,
                                              square_pitroom,
                                              skeletons, mundane_items,
                                              no_characters, no_items,
                                              altar_items,
                                              square_library, circular_library,
                                              circular_cache_room,
                                              circular_band_room,
                                              square_band_room,
                                              square_banded_library,
                                              circular_room_with_candles)
from pyherc.config.dsl import LevelConfiguration, LevelContext
from pyherc.data import add_location_feature, floor_tile
from pyherc.data.effects import DamageModifier
from pyherc.data.features import new_cache
from pyherc.generators import creature_config, inventory_config
from pyherc.generators.level.creatures import (CreatureAdder,
                                               CreatureAdderConfiguration)
from pyherc.generators.level.decorator import (AggregateDecorator,
                                               AggregateDecoratorConfig,
                                               DirectionalWallDecorator,
                                               DirectionalWallDecoratorConfig,
                                               FloorBuilderDecorator,
                                               FloorBuilderDecoratorConfig,
                                               ReplacingDecorator,
                                               ReplacingDecoratorConfig,
                                               SurroundingDecorator,
                                               SurroundingDecoratorConfig,
                                               WallBuilderDecorator,
                                               WallBuilderDecoratorConfig,
                                               WallOrnamentDecorator,
                                               WallOrnamentDecoratorConfig)
from pyherc.generators.level import ItemAdder, ItemAdderConfiguration
from pyherc.generators.level import PortalAdderConfiguration
from pyherc.generators.level import new_dungeon, new_level, add_level
from pyherc.generators.level.partitioners import binary_space_partitioning
from pyherc.generators.level.room import (PillarRoomGenerator,
                                          TempleRoomGenerator)
from pyherc.rules.constants import (CRUSHING_DAMAGE, LIGHT_DAMAGE,
                                    PIERCING_DAMAGE, POISON_DAMAGE)


def init_level(rng, item_generator, creature_generator, level_size, context):
    """
    Initialise upper catacombs

    :returns: level configuration
    :rtype: LevelConfiguration
    """
    surface_manager = context.surface_manager

    tile_floor = 'tile floor'

    wall_empty = None
    floor_empty = None
    wall_natural = 'natural wall'
    wall_constructed = 'constructed wall'
    wall = 'wall'

    stairs_down = surface_manager.add_icon('stairs_down',
                                           ':stairs_down.png',
                                           '>')
    stairs_up = surface_manager.add_icon('stairs_up',
                                         ':stairs_up.png',
                                         '<')

    pillar = surface_manager.add_icon('pillar', ':pillar.png', '#')

    wall_15 = surface_manager.add_icon('wall_rubble6_15',
                                       ':walls/wall_rubble6_15.png', '#')
    wall_57 = surface_manager.add_icon('wall_rubble6_57',
                                       ':walls/wall_rubble6_57.png', '#')
    wall_35 = surface_manager.add_icon('wall_rubble6_35',
                                       ':walls/wall_rubble6_35.png', '#')
    wall_37 = surface_manager.add_icon('wall_rubble6_37',
                                       ':walls/wall_rubble6_37.png', '#')
    wall_17 = surface_manager.add_icon('wall_rubble6_17',
                                       ':walls/wall_rubble6_17.png', '#')
    wall_13 = surface_manager.add_icon('wall_rubble6_13',
                                       ':walls/wall_rubble6_13.png', '#')

    wall_135 = surface_manager.add_icon('wall_rubble6_135',
                                        ':walls/wall_rubble6_135.png', '#')
    wall_357 = surface_manager.add_icon('wall_rubble6_357',
                                        ':walls/wall_rubble6_357.png', '#')
    wall_1357 = surface_manager.add_icon('wall_rubble6_1357',
                                         ':walls/wall_rubble6_1357.png', '#')
    wall_137 = surface_manager.add_icon('wall_rubble6_137',
                                        ':walls/wall_rubble6_137.png', '#')
    wall_157 = surface_manager.add_icon('wall_rubble6_157',
                                        ':walls/wall_rubble6_157.png', '#')

    altar = surface_manager.add_icon('altar', ':altar.png', '_')

    rooms = [          PillarRoomGenerator(floor_tile = tile_floor,
                                           corridor_tile = tile_floor,
                                           empty_tile = wall_empty,
                                           pillar_tile = pillar,
                                           level_types = ['first gate']),
                       TempleRoomGenerator(tile_floor,
                                           tile_floor,
                                           altar,
                                           ['first gate'],
                                           ['standing_candle_f0',
                                            'standing_candle_f1']),
                       TempleRoomGenerator(tile_floor,
                                           tile_floor,
                                           ["fountain_f0",
                                            "fountain_f1"],
                                           ['first gate'])]

    tomb_stones = ['tomb 1', 'tomb 2', 'tomb 3', 'tomb 4', 'tomb 5',
                   'tomb 6', 'tomb 7', 'tomb 8', 'tomb 9']
    book_shelves = ['shelf 1', 'shelf 2', 'shelf 3']
    standing_candles = ['standing_candle_f0', 'standing_candle_f1']

    rooms = [circular_room('ground_tile3', tile_floor, rng),
             square_room('ground_tile3', tile_floor, rng),
             square_room(tile_floor, tile_floor, rng),             
             circular_room(tile_floor, tile_floor, rng),
             circular_band_room('ground_tile3', tile_floor, tile_floor, rng),
             square_band_room('ground_tile3', tile_floor, tile_floor, rng),
             circular_graveyard(tile_floor, tile_floor,
                                tomb_stones,
                                mundane_items(50, item_generator, rng), 
                                skeletons(50, creature_generator, rng), rng),
             square_graveyard(tile_floor, tile_floor,
                              tomb_stones,
                              mundane_items(50, item_generator, rng), 
                              skeletons(50, creature_generator, rng), rng),
             square_library('ground_tile3', tile_floor, book_shelves, rng),
             circular_library('ground_tile3', tile_floor, book_shelves, rng),
             square_banded_library('ground_tile3', tile_floor, tile_floor,
                                   book_shelves, rng),
             circular_cache_room(tile_floor, tile_floor, [altar], 
                                 altar_items(50, item_generator, rng),
                                 no_characters(), rng),
             circular_room_with_candles('ground_wood4', tile_floor, tile_floor, 
                                        [standing_candles], rng)]

    level_partitioners = [binary_space_partitioning((80, 40), (11, 11), rng)]

    surrounder_config = SurroundingDecoratorConfig(['first gate'],
                                                   wall_natural)
    surrounder = SurroundingDecorator(surrounder_config)

    wallbuilder_config = WallBuilderDecoratorConfig(['first gate'],
                                        {wall_natural: wall_constructed},
                                         wall_empty)
    wallbuilder = WallBuilderDecorator(wallbuilder_config)

    wall_direction_config = DirectionalWallDecoratorConfig(['first gate'],
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

    floor = surface_manager.add_icon('ground_soil4',
                                     ':ground/ground_soil4.png', ' ')
    floor1 = surface_manager.add_icon('ground_soil4_1',
                                      ':ground/ground_soil4_1.png', ' ')
    floor3 = surface_manager.add_icon('ground_soil4_3',
                                      ':ground/ground_soil4_3.png', ' ')
    floor5 = surface_manager.add_icon('ground_soil4_5',
                                      ':ground/ground_soil4_5.png', ' ')
    floor7 = surface_manager.add_icon('ground_soil4_7',
                                      ':ground/ground_soil4_7.png', ' ')
    floor13 = surface_manager.add_icon('ground_soil4_13',
                                       ':ground/ground_soil4_13.png', ' ')
    floor15 = surface_manager.add_icon('ground_soil4_15',
                                       ':ground/ground_soil4_15.png', ' ')
    floor17 = surface_manager.add_icon('ground_soil4_17',
                                       ':ground/ground_soil4_17.png', ' ')
    floor35 = surface_manager.add_icon('ground_soil4_35',
                                       ':ground/ground_soil4_35.png', ' ')
    floor37 = surface_manager.add_icon('ground_soil4_37',
                                       ':ground/ground_soil4_37.png', ' ')
    floor57 = surface_manager.add_icon('ground_soil4_57',
                                       ':ground/ground_soil4_57.png', ' ')
    floor135 = surface_manager.add_icon('ground_soil4_135',
                                        ':ground/ground_soil4_135.png', ' ')
    floor137 = surface_manager.add_icon('ground_soil4_137',
                                        ':ground/ground_soil4_137.png', ' ')
    floor157 = surface_manager.add_icon('ground_soil4_157',
                                        ':ground/ground_soil4_157.png', ' ')
    floor357 = surface_manager.add_icon('ground_soil4_357',
                                        ':ground/ground_soil4_357.png', ' ')
    floor1357 = surface_manager.add_icon('ground_soil4_1357',
                                         ':ground/ground_soil4_1357.png', ' ')

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
                                               floor = tile_floor,
                                               nook_west = floor1357,
                                               nook_east = floor1357)
    floor_builder = FloorBuilderDecorator(floor_config)

    tile3_floor = FloorBuilderDecoratorConfig([],
                                               single = 'ground_tile3',
                                               north = 'ground_tile3_1',
                                               east = 'ground_tile3_3',
                                               south = 'ground_tile3_5',
                                               west = 'ground_tile3_7',
                                               north_east = 'ground_tile3_13',
                                               north_south = 'ground_tile3_15',
                                               north_west = 'ground_tile3_17',
                                               east_south = 'ground_tile3_35',
                                               east_west = 'ground_tile3_37',
                                               south_west = 'ground_tile3_57',
                                               north_east_south = 'ground_tile3_135',
                                               north_east_west = 'ground_tile3_137',
                                               north_south_west = 'ground_tile3_157',
                                               east_south_west = 'ground_tile3_357',
                                               fourway = 'ground_tile3_1357',
                                               floor = 'ground_tile3',
                                               nook_west = 'ground_tile3_1357',
                                               nook_east = 'ground_tile3_1357')
    tile3_floor_builder = FloorBuilderDecorator(tile3_floor)

    tile4_floor = FloorBuilderDecoratorConfig([],
                                               single = 'ground_tile4',
                                               north = 'ground_tile4_1',
                                               east = 'ground_tile4_3',
                                               south = 'ground_tile4_5',
                                               west = 'ground_tile4_7',
                                               north_east = 'ground_tile4_13',
                                               north_south = 'ground_tile4_15',
                                               north_west = 'ground_tile4_17',
                                               east_south = 'ground_tile4_35',
                                               east_west = 'ground_tile4_37',
                                               south_west = 'ground_tile4_57',
                                               north_east_south = 'ground_tile4_135',
                                               north_east_west = 'ground_tile4_137',
                                               north_south_west = 'ground_tile4_157',
                                               east_south_west = 'ground_tile4_357',
                                               fourway = 'ground_tile4_1357',
                                               floor = 'ground_tile4',
                                               nook_west = 'ground_tile4_1357',
                                               nook_east = 'ground_tile4_1357')
    tile4_floor_builder = FloorBuilderDecorator(tile4_floor)

    wood4_floor = FloorBuilderDecoratorConfig([],
                                              single = 'ground_wood4',
                                              north = 'ground_wood4_1',
                                              east = 'ground_wood4_3',
                                              south = 'ground_wood4_5',
                                              west = 'ground_wood4_7',
                                              north_east = 'ground_wood4_13',
                                              north_south = 'ground_wood4_15',
                                              north_west = 'ground_wood4_17',
                                              east_south = 'ground_wood4_35',
                                              east_west = 'ground_wood4_37',
                                              south_west = 'ground_wood4_57',
                                              north_east_south = 'ground_wood4_135',
                                              north_east_west = 'ground_wood4_137',
                                              north_south_west = 'ground_wood4_157',
                                              east_south_west = 'ground_wood4_357',
                                              fourway = 'ground_wood4_1357',
                                              floor = 'ground_wood4',
                                              nook_west = 'ground_wood4_1357',
                                              nook_east = 'ground_wood4_1357')
    wood4_floor_builder = FloorBuilderDecorator(wood4_floor)
    
    torches_tile_f0 = surface_manager.add_icon('catacombs_torches_f0',
                                               ':wall_torches_f0.png', '¤')
    torches_tile_f1 = surface_manager.add_icon('catacombs_torches_f1',
                                               ':wall_torches_f1.png', '¤')
    torch_tile_f0 = surface_manager.add_icon('catacombs_torch_f0',
                                             ':wall_torch_f0.png', '¤')
    torch_tile_f1 = surface_manager.add_icon('catacombs_torch_f1',
                                             ':wall_torch_f1.png', '¤')

    torch_ornamenter_config = WallOrnamentDecoratorConfig(
                                                ['first gate'],
                                                wall_tile = wall_37,
                                                ornamentation = [(torch_tile_f0, torch_tile_f1),
                                                                 (torches_tile_f0, torches_tile_f1)],
                                                rng = rng,
                                                rate = 10)
    torch_ornamenter = WallOrnamentDecorator(torch_ornamenter_config)

    aggregate_decorator_config = AggregateDecoratorConfig(
                                                ['first gate'],
                                                [surrounder,
                                                 wallbuilder,
                                                 wall_direction_builder,
                                                 floor_builder,
                                                 tile3_floor_builder,
                                                 tile4_floor_builder,
                                                 wood4_floor_builder,
                                                 torch_ornamenter])

    decorators = [AggregateDecorator(aggregate_decorator_config)]

    item_adder_config = ItemAdderConfiguration(['first gate'])

    item_adders = [ItemAdder(item_generator,
                            item_adder_config,
                            rng)]

    creatures_upper = CreatureAdderConfiguration(['first gate'])
    creatures_upper.add_creature(min_amount = 4,
                                 max_amount = 8,
                                 name = 'rat')
    creatures_upper.add_creature(min_amount = 1,
                                 max_amount = 2,
                                 name = 'fire beetle')
    creatures_upper.add_creature(min_amount = 0,
                                 max_amount = 1,
                                 name = 'skeleton warrior')

    creature_adders = [CreatureAdder(creature_generator,
                                    creatures_upper,
                                    rng)]

    portal_adder_configurations = [PortalAdderConfiguration(
                                        icons = (stairs_up,
                                                 stairs_down),
                                        level_type = 'first gate',
                                        location_type = 'room',
                                        chance = 100,
                                        new_level = 'lower catacombs',
                                        unique = True)]

    level_context = LevelContext(size = level_size,
                                 floor_type = floor_empty,
                                 wall_type = wall_natural,
                                 level_types = ['first gate'])

    return [new_level('first gate', rooms, level_partitioners,
                      decorators, item_adders, creature_adders,
                      portal_adder_configurations)]

    return config

def init_creatures(context):
    """
    Initialise creatures''

    :returns: list of configuration items
    :rtype: [CreatureConfiguration]
    """
    surface_manager = context.surface_manager
    config = []

    fungus_f0 = surface_manager.add_icon('fungus_f0',
                                         ':fungus_f0.png',
                                         'F', ['yellow', 'dim'])
    fungus_f1 = surface_manager.add_icon('fungus_f1',
                                         ':fungus_f1.png',
                                         'F', ['yellow', 'dim'])
    config.append(creature_config(name = 'fungus',
                                  body = 4,
                                  finesse = 2,
                                  mind = 1,
                                  hp = 7,
                                  speed = 8,
                                  icons = (fungus_f0, fungus_f1),
                                  attack = 3,
                                  ai = FungusAI))

    great_fungus_f0 = surface_manager.add_icon('great_fungus_f0',
                                               ':great_fungus_f0.png', 
                                               'F', ['white', 'bold'])
    great_fungus_f1 = surface_manager.add_icon('great_fungus_f1',
                                               ':great_fungus_f1.png',
                                               'F', ['white', 'bold'])
    config.append(creature_config(name = 'great fungus',
                                  body = 6,
                                  finesse = 1,
                                  mind = 3,
                                  hp = 12,
                                  speed = 8,
                                  icons = (great_fungus_f0, great_fungus_f1),
                                  attack = 5,
                                  ai = GreatFungusAI))
    return config
