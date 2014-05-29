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
module for configuring catacombs
"""
import hy
from herculeum.ai import FlockingHerbivore, SkeletonWarriorAI
from herculeum.ai.firebeetle import FireBeetleAI
from herculeum.ai.rat import RatAI
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
from pyherc.generators.level.room import CatacombsGenerator
from pyherc.rules.constants import (CRUSHING_DAMAGE, LIGHT_DAMAGE,
                                    PIERCING_DAMAGE, POISON_DAMAGE)


def init_level(rng, item_generator, creature_generator, level_size, context):
    """
    Initialise upper catacombs

    :returns: level configuration
    :rtype: LevelConfiguration
    """
    surface_manager = context.surface_manager

    floor_natural = 'natural floor'
    floor_rock = surface_manager.add_icon('floor_rock',
                                          ':rock_floor.png',
                                          '.')

    wall_empty = None
    floor_empty = None

    wall_natural = 'natural wall'
    wall_constructed = 'constructed wall'
    wall_ground = surface_manager.add_icon('wall_ground',
                                           ':ground_wall.png',
                                           ' ')
    wall_rock = surface_manager.add_icon('wall_rock',
                                         ':rock_wall.png',
                                         '#')
    stairs_down = surface_manager.add_icon('stairs_down',
                                           ':stairs_down.png',
                                           '>')
    stairs_up = surface_manager.add_icon('stairs_up',
                                         ':stairs_up.png',
                                         '<')

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

    room_generators = [CatacombsGenerator(floor_natural,
                                           wall_empty,
                                           ['upper catacombs',
                                           'lower catacombs'],
                                           rng)]
    level_partitioners = [GridPartitioner(['upper catacombs',
                                           'lower catacombs'],
                                           1,
                                           1,
                                           rng)]

    replacer_config = ReplacingDecoratorConfig(['upper catacombs',
                                                'lower catacombs'],
                                    {floor_natural: floor_rock},
                                    {wall_natural: wall_ground,
                                    wall_constructed: wall_rock})
    replacer = ReplacingDecorator(replacer_config)

    surrounder_config = SurroundingDecoratorConfig(['upper catacombs',
                                                    'lower catacombs'],
                                                   wall_natural)
    surrounder = SurroundingDecorator(surrounder_config)

    wallbuilder_config = WallBuilderDecoratorConfig(['upper catacombs',
                                                    'lower catacombs'],
                                        {wall_natural: wall_constructed},
                                         wall_empty)
    wallbuilder = WallBuilderDecorator(wallbuilder_config)

    wall_direction_config = DirectionalWallDecoratorConfig(['upper catacombs'],
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
                                               floor = floor_natural)
    floor_builder = FloorBuilderDecorator(floor_config)

    torches_tile_f0 = surface_manager.add_icon('catacombs_torches_f0', ':wall_torches_f0.png', '¤')
    torches_tile_f1 = surface_manager.add_icon('catacombs_torches_f1', ':wall_torches_f1.png', '¤')
    torch_tile_f0 = surface_manager.add_icon('catacombs_torch_f0', ':wall_torch_f0.png', '¤')
    torch_tile_f1 = surface_manager.add_icon('catacombs_torch_f1', ':wall_torch_f1.png', '¤')

    torch_ornamenter_config = WallOrnamentDecoratorConfig(
                                                ['upper catacombs',
                                                 'lower catacombs'],
                                                wall_tile = wall_37,
                                                ornamentation = [(torch_tile_f0, torch_tile_f1),
                                                                 (torches_tile_f0, torches_tile_f1)],
                                                rng = rng,
                                                rate = 10)
    torch_ornamenter = WallOrnamentDecorator(torch_ornamenter_config)

    aggregate_decorator_config = AggregateDecoratorConfig(
                                                ['upper catacombs',
                                                'lower catacombs'],
                                                [surrounder,
                                                 wallbuilder,
                                                 wall_direction_builder,
                                                 floor_builder,
                                                 torch_ornamenter,
                                                 replacer])

    decorators = [AggregateDecorator(aggregate_decorator_config)]

    item_adder_config = ItemAdderConfiguration(['upper catacombs',
                                               'lower catacombs'])
    item_adder_config.add_item(min_amount = 0,
                               max_amount = 4,
                               type = 'weapon',
                               location = 'room')
    item_adder_config.add_item(min_amount = 0,
                               max_amount = 2,
                               type = 'potion',
                               location = 'room')
    item_adder_config.add_item(min_amount = 1,
                               max_amount = 3,
                               type = 'food',
                               location = 'room')
    item_adder_config.add_item(min_amount = 0,
                               max_amount = 2,
                               type = 'armour',
                               location = 'room')
    item_adder_config.add_item(min_amount = 0,
                               max_amount = 1,
                               type = 'tome',
                               location = 'room')
    item_adders = [ItemAdder(item_generator,
                            item_adder_config,
                            rng)]

    creatures_upper = CreatureAdderConfiguration(['upper catacombs'])
    creatures_upper.add_creature(min_amount = 6,
                                 max_amount = 12,
                                 name = 'rat')
    creatures_upper.add_creature(min_amount = 0,
                                 max_amount = 1,
                                 name = 'skeleton warrior')

    creatures_lower = CreatureAdderConfiguration(['lower catacombs'])
    creatures_lower.add_creature(min_amount = 6,
                                 max_amount = 12,
                                 name = 'rat')
    creatures_lower.add_creature(min_amount = 2,
                                 max_amount = 5,
                                 name = 'fire beetle')
    creatures_lower.add_creature(min_amount = 1,
                                 max_amount = 3,
                                 name = 'skeleton warrior')

    creature_adders = [CreatureAdder(creature_generator,
                                    creatures_upper,
                                    rng),
                       CreatureAdder(creature_generator,
                                    creatures_lower,
                                    rng)
                                    ]

    portal_adder_configurations = [PortalAdderConfiguration(
                                        icons = (stairs_up,
                                                 stairs_down),
                                        level_type = 'lower catacombs',
                                        location_type = 'room',
                                        chance = 100,
                                        new_level = 'upper catacombs',
                                        unique = True),
                                    PortalAdderConfiguration(
                                        icons = (stairs_up,
                                                 stairs_down),
                                        level_type = 'upper catacombs',
                                        location_type = 'room',
                                        chance = 100,
                                        new_level = '',
                                        unique = True,
                                        escape_stairs = True)
                                        ]

    level_context = LevelContext(size = level_size,
                                 floor_type = floor_empty,
                                 wall_type = wall_natural,
                                 level_types = ['upper catacombs',
                                                'lower catacombs'])

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

    mouse_f0 = surface_manager.add_icon('rat_f0', ':mouse_f0.png', 'r', ['yellow', 'dim'])
    mouse_f1 = surface_manager.add_icon('rat_f1', ':mouse_f1.png', 'r', ['yellow', 'dim'])
    config.append(creature_config(name = 'rat',
                                  body = 4,
                                  finesse = 12,
                                  mind = 2,
                                  hp = 2,
                                  speed = 2,
                                  icons = (mouse_f0, mouse_f1),
                                  attack = 1,
                                  ai = RatAI))

    firebeetle_f0 = surface_manager.add_icon('fire beetle_f0', ':scarab-beetle_f0.png', 'a', ['red'])
    firebeetle_f1 = surface_manager.add_icon('fire beetle_f1', ':scarab-beetle_f1.png', 'a', ['red'])
    config.append(creature_config(name = 'fire beetle',
                                  body = 10,
                                  finesse = 11,
                                  mind = 0,
                                  hp = 4,
                                  speed = 3,
                                  icons = (firebeetle_f0, firebeetle_f1),
                                  attack = 2,
                                  ai = FireBeetleAI))

    skeleton_inventory = [inventory_config(item_name = 'sword',
                                           min_amount = 0,
                                           max_amount = 1,
                                           probability = 100)]

    skeleton_effects = [DamageModifier(modifier = 2,
                                       damage_type = CRUSHING_DAMAGE,
                                       duration = None,
                                       frequency = None,
                                       tick = None,
                                       icon = 0,
                                       title = '',
                                       description = ''),
                        DamageModifier(modifier = 2,
                                       damage_type = LIGHT_DAMAGE,
                                       duration = None,
                                       frequency = None,
                                       tick = None,
                                       icon = 0,
                                       title = '',
                                       description = ''),
                        DamageModifier(modifier = -2,
                                       damage_type = PIERCING_DAMAGE,
                                       duration = None,
                                       frequency = None,
                                       tick = None,
                                       icon = 0,
                                       title = '',
                                       description = ''),
                        DamageModifier(modifier = -2,
                                       damage_type = POISON_DAMAGE,
                                       duration = None,
                                       frequency = None,
                                       tick = None,
                                       icon = 0,
                                       title = '',
                                       description = '')]

    skeleton_f0 = surface_manager.add_icon('skeleton warrior_f0', ':blade-bite_f0.png', 'Z', ['white', 'bold'])
    skeleton_f1 = surface_manager.add_icon('skeleton warrior_f1', ':blade-bite_f1.png', 'Z', ['white', 'bold'])
    config.append(creature_config(name = 'skeleton warrior',
                                  body = 8,
                                  finesse = 11,
                                  mind = 0,
                                  hp = 8,
                                  speed = 4,
                                  icons = (skeleton_f0, skeleton_f1),
                                  attack = 1,
                                  ai = SkeletonWarriorAI,
                                  inventory = skeleton_inventory,
                                  effects = skeleton_effects))

    return config
