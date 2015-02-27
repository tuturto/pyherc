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
from herculeum.config.floor_builders import (soil3_floorbuilder,
                                             soil4_floorbuilder,
                                             tile3_floorbuilder,
                                             tile4_floorbuilder,
                                             wood4_floorbuilder)
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
                                              circular_room_with_candles,
                                              circular_bones_room,
                                              pillar_room)
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
                                               SurroundingDecorator,
                                               SurroundingDecoratorConfig,
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

    wall_natural = 'natural wall'
    wall = 'wall'

    stairs_down = surface_manager.add_icon('stairs_down',
                                           ':stairs_down.png',
                                           '>')
    stairs_up = surface_manager.add_icon('stairs_up',
                                         ':stairs_up.png',
                                         '<')

    pillar = surface_manager.add_icon('pillar', ':pillar.png', '#')

    surface_manager.add_icon('wall_rubble6', ':walls/wall_rubble6.png', '#')
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

    rooms = [TempleRoomGenerator('ground_soil4',
                                 'ground_soil4',
                                 altar,
                                 ['first gate'],
                                 ['standing_candle_f0',
                                  'standing_candle_f1']),
             TempleRoomGenerator('ground_soil4',
                                 'ground_soil4',
                                 ["fountain_f0",
                                  "fountain_f1"],
                                 ['first gate'])]
    
    tomb_stones = ['tomb 1', 'tomb 2', 'tomb 3', 'tomb 4', 'tomb 5',
                   'tomb 6', 'tomb 7', 'tomb 8', 'tomb 9']
    book_shelves = ['shelf 1', 'shelf 2', 'shelf 3']
    standing_candles = ['standing_candle_f0', 'standing_candle_f1']
    bones = ['bones 1', 'bones 2', 'skull 1', 'skull 2']

    rooms = [circular_room('ground_tile3', 'ground_soil4', rng),
             square_room('ground_tile3', 'ground_soil4', rng),
             square_room('ground_soil4', 'ground_soil4', rng),             
             circular_room('ground_soil4', 'ground_soil4', rng),
             circular_band_room('ground_tile3', 'ground_soil4', 'ground_soil4',
                                rng),
             square_band_room('ground_tile3', 'ground_soil4', 'ground_soil4',
                              rng),
             circular_graveyard('ground_soil4', 'ground_soil4',
                                tomb_stones,
                                mundane_items(50, item_generator, rng), 
                                skeletons(50, creature_generator, rng), rng),
             square_graveyard('ground_soil4', 'ground_soil4',
                              tomb_stones,
                              mundane_items(50, item_generator, rng), 
                              skeletons(50, creature_generator, rng), rng),
             square_library('ground_tile3', 'ground_soil4', book_shelves, rng),
             circular_library('ground_tile3', 'ground_soil4', book_shelves,
                              rng),
             square_banded_library('ground_tile3', 'ground_soil4',
                                   'ground_soil4', book_shelves, rng),
             circular_cache_room('ground_soil4', 'ground_soil4', [altar], 
                                 altar_items(50, item_generator, rng),
                                 no_characters(), rng),
             circular_room_with_candles('ground_wood4', 'ground_soil4',
                                        'ground_soil4', [standing_candles],
                                        rng),
             circular_bones_room('ground_soil3', 'ground_soil4',
                                 'ground_soil4', bones, 25, rng),
             pillar_room('ground_tile3', 'ground_soil4', ['statue'], rng),
             pillar_room('ground_tile3', 'ground_soil4', ['wall_rubble6'], rng),
             pillar_room('ground_soil4', 'ground_soil4', ['wall_rubble6'], rng)]

    level_partitioners = [binary_space_partitioning((80, 40), (11, 11), rng)]

    surrounder_config = SurroundingDecoratorConfig(['first gate'],
                                                   'wall_rubble6')
    surrounder = SurroundingDecorator(surrounder_config)

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
                                                   wall = 'wall_rubble6')

    wall_direction_builder = DirectionalWallDecorator(wall_direction_config)
    
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
    moss_ornamenter = WallOrnamentDecorator(
        WallOrnamentDecoratorConfig([],
                                    wall_tile = wall_37,
                                    ornamentation = ['wall moss 1', 
                                                     'wall moss 2'],
                                    rng = rng,
                                    rate = 30))
    crack_ornamenter = WallOrnamentDecorator(
        WallOrnamentDecoratorConfig([],
                                    wall_tile = wall_37,
                                    ornamentation = ['wall crack 1', 
                                                     'wall crack 2'],
                                    rng = rng,
                                    rate = 30))

    beams_1_ornamenter = WallOrnamentDecorator(
        WallOrnamentDecoratorConfig([],
                                    wall_tile = wall_37,
                                    ornamentation = ['wooden beams 1'],
                                    rng = rng,
                                    rate = 10,
                                    top_only = False))

    beams_2_ornamenter = WallOrnamentDecorator(
        WallOrnamentDecoratorConfig([],
                                    wall_tile = wall_15,
                                    ornamentation = ['wooden beams 2',
                                                     'wooden beams 3',
                                                     'wooden beams 4'],
                                    rng = rng,
                                    rate = 10,
                                    top_only = False))



    aggregate_decorator_config = AggregateDecoratorConfig(
                                                ['first gate'],
                                                [surrounder,
                                                 wall_direction_builder,
                                                 soil3_floorbuilder,
                                                 soil4_floorbuilder,
                                                 tile3_floorbuilder,
                                                 tile4_floorbuilder,
                                                 wood4_floorbuilder,
                                                 crack_ornamenter,
                                                 beams_1_ornamenter,
                                                 beams_2_ornamenter,
                                                 moss_ornamenter,
                                                 torch_ornamenter])

    decorators = [AggregateDecorator(aggregate_decorator_config)]

    item_adder_config = ItemAdderConfiguration(['first gate'])

    item_adder_config.add_item(min_amount = 0,
                               max_amount = 1,
                               type = 'tome',
                               location = 'room')

    item_adder_config.add_item(min_amount = 0,
                               max_amount = 2,
                               type = 'weapon',
                               location = 'room')

    item_adder_config.add_item(min_amount = 2,
                               max_amount = 4,
                               type = 'food',
                               location = 'room')

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
