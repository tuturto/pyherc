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

from herculeum.config.floor_builders import floor_builder
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
from pyherc.generators.level.decorator import (DirectionalWallDecorator,
                                               DirectionalWallDecoratorConfig,
                                               SurroundingDecorator,
                                               SurroundingDecoratorConfig,
                                               WallOrnamentDecorator,
                                               WallOrnamentDecoratorConfig,
                                               wall_ornamenter)
from pyherc.generators.level import (item_by_type, item_lists, creature_lists,
                                     creature)
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
    altar = surface_manager.add_icon('altar', ':altar.png', '_')

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

    moss_ornamenter = wall_ornamenter([wall_15, ['wall moss 4']],
                                      [wall_37, ['wall moss 1',
                                                 'wall moss 2']],
                                      [wall_15, ['wall moss 3']],
                                      30, rng)
    
    decorators = [moss_ornamenter]
    
    return [new_level('first gate', rooms, level_partitioners,
                      decorators, item_adders, creature_adders,
                      portal_adder_configurations)]
