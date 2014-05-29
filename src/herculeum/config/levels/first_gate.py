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
module for configuring first gate
"""
import hy
from herculeum.ai.fungus import FungusAI, GreatFungusAI
from pyherc.config.dsl import LevelConfiguration, LevelContext
from pyherc.data.effects import DamageModifier
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
from pyherc.generators.level.items import ItemAdder, ItemAdderConfiguration
from pyherc.generators.level.partitioners import GridPartitioner
from pyherc.generators.level.portals import PortalAdderConfiguration
from pyherc.generators.level.room import (PillarRoomGenerator,
                                          SquareRoomGenerator)
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

    wall_15 = surface_manager.add_icon('catacombs_wall_15', ':catacombs_wall_2_8.png', '#')
    wall_57 = surface_manager.add_icon('catacombs_wall_57', ':catacombs_wall_2_4.png', '#')
    wall_35 = surface_manager.add_icon('catacombs_wall_35', ':catacombs_wall_2_6.png', '#')
    wall_37 = surface_manager.add_icon('catacombs_wall_37', ':catacombs_wall_4_6.png', '#')
    wall_17 = surface_manager.add_icon('catacombs_wall_17', ':catacombs_wall_8_4.png', '#')
    wall_13 = surface_manager.add_icon('catacombs_wall_13', ':catacombs_wall_8_6.png', '#')

    wall_135 = surface_manager.add_icon('catacombs_wall_135', ':catacombs_wall_2_6_8.png', '#')
    wall_357 = surface_manager.add_icon('catacombs_wall_357', ':catacombs_wall_2_4_6.png', '#')
    wall_1357 = surface_manager.add_icon('catacombs_wall_1357', ':catacombs_wall_2_4_6_8.png', '#')
    wall_137 = surface_manager.add_icon('catacombs_wall_137', ':catacombs_wall_4_6_8.png', '#')
    wall_157 = surface_manager.add_icon('catacombs_wall_157', ':catacombs_wall_2_4_8.png', '#')

    room_generators = [SquareRoomGenerator(tile_floor,
                                           wall_empty,
                                           tile_floor,
                                           ['first gate']),
                       PillarRoomGenerator(floor_tile = tile_floor,
                                           corridor_tile = tile_floor,
                                           empty_tile = wall_empty,
                                           pillar_tile = pillar,
                                           level_types = ['first gate'])]

    level_partitioners = [GridPartitioner(['first gate'],
                                           3,
                                           2,
                                           rng)]

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

    floor = surface_manager.add_icon('catacombs_floor', ':catacombs_floor.png', ' ')
    floor1 = surface_manager.add_icon('catacombs_floor_1', ':catacombs_floor_1.png', ' ')
    floor3 = surface_manager.add_icon('catacombs_floor_3', ':catacombs_floor_3.png', ' ')
    floor5 = surface_manager.add_icon('catacombs_floor_5', ':catacombs_floor_5.png', ' ')
    floor7 = surface_manager.add_icon('catacombs_floor_7', ':catacombs_floor_7.png', ' ')
    floor13 = surface_manager.add_icon('catacombs_floor_13', ':catacombs_floor_13.png', ' ')
    floor15 = surface_manager.add_icon('catacombs_floor_15', ':catacombs_floor_15.png', ' ')
    floor17 = surface_manager.add_icon('catacombs_floor_17', ':catacombs_floor_17.png', ' ')
    floor35 = surface_manager.add_icon('catacombs_floor_35', ':catacombs_floor_35.png', ' ')
    floor37 = surface_manager.add_icon('catacombs_floor_37', ':catacombs_floor_37.png', ' ')
    floor57 = surface_manager.add_icon('catacombs_floor_57', ':catacombs_floor_57.png', ' ')
    floor135 = surface_manager.add_icon('catacombs_floor_135', ':catacombs_floor_135.png', ' ')
    floor137 = surface_manager.add_icon('catacombs_floor_137', ':catacombs_floor_137.png', ' ')
    floor157 = surface_manager.add_icon('catacombs_floor_157', ':catacombs_floor_157.png', ' ')
    floor357 = surface_manager.add_icon('catacombs_floor_357', ':catacombs_floor_357.png', ' ')
    floor1357 = surface_manager.add_icon('catacombs_floor_1357', ':catacombs_floor_1357.png', ' ')

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
                                               floor = tile_floor)
    floor_builder = FloorBuilderDecorator(floor_config)

    torches_tile_f0 = surface_manager.add_icon('catacombs_torches_f0', ':wall_torches_f0.png', '¤')
    torches_tile_f1 = surface_manager.add_icon('catacombs_torches_f1', ':wall_torches_f1.png', '¤')
    torch_tile_f0 = surface_manager.add_icon('catacombs_torch_f0', ':wall_torch_f0.png', '¤')
    torch_tile_f1 = surface_manager.add_icon('catacombs_torch_f1', ':wall_torch_f1.png', '¤')

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
                                                 torch_ornamenter])

    decorators = [AggregateDecorator(aggregate_decorator_config)]

    item_adder_config = ItemAdderConfiguration(['first gate'])

    item_adders = [ItemAdder(item_generator,
                            item_adder_config,
                            rng)]

    creatures_upper = CreatureAdderConfiguration(['first gate'])
    creatures_upper.add_creature(min_amount = 3,
                                 max_amount = 6,
                                 name = 'rat')
    creatures_upper.add_creature(min_amount = 0,
                                 max_amount = 1,
                                 name = 'fire beetle')
    creatures_upper.add_creature(min_amount = 0,
                                 max_amount = 1,
                                 name = 'skeleton warrior')
    creatures_upper.add_creature(min_amount = 3,
                                 max_amount = 6,
                                 name = 'fungus')

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
    Initialise creatures''

    :returns: list of configuration items
    :rtype: [CreatureConfiguration]
    """
    surface_manager = context.surface_manager
    config = []

    fungus_f0 = surface_manager.add_icon('fungus_f0', ':fungus_f0.png', 'F', ['yellow', 'dim'])
    fungus_f1 = surface_manager.add_icon('fungus_f1', ':fungus_f1.png', 'F', ['yellow', 'dim'])
    config.append(creature_config(name = 'fungus',
                                  body = 4,
                                  finesse = 2,
                                  mind = 1,
                                  hp = 7,
                                  speed = 8,
                                  icons = (fungus_f0, fungus_f1),
                                  attack = 3,
                                  ai = FungusAI))

    great_fungus_f0 = surface_manager.add_icon('great_fungus_f0', ':great_fungus_f0.png', 'F', ['white', 'bold'])
    great_fungus_f1 = surface_manager.add_icon('great_fungus_f1', ':great_fungus_f1.png', 'F', ['white', 'bold'])
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
