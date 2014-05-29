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
module for configuring lair of crimson jaw
"""
from herculeum.ai import SkeletonWarriorAI
from pyherc.config.dsl import LevelConfiguration, LevelContext
from pyherc.data.effects import EffectHandle
from pyherc.generators import (creature_config, inventory_config,
                               ItemConfiguration, WeaponConfiguration)
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
                                               WallBuilderDecoratorConfig)
from pyherc.generators.level.items import ItemAdder, ItemAdderConfiguration
from pyherc.generators.level.partitioners import GridPartitioner
from pyherc.generators.level.portals import PortalAdderConfiguration
from pyherc.generators.level.room import CrimsonLairGenerator
from pyherc.rules.constants import SLASHING_DAMAGE


def init_level(rng, item_generator, creature_generator, level_size, context):
    """
    Initialise lair of crimson jaw

    :returns: level configuration
    :rtype: LevelConfiguration
    """
    surface_manager = context.surface_manager

    floor_natural = 'natural floor'
    floor_rock = surface_manager.add_icon('floor_rock', ':rock_floor.png', '.')

    wall_empty = None
    wall_natural = 'natural wall'
    wall_constructed = 'constructed wall'
    wall_ground = surface_manager.add_icon('wall_ground', ':ground_wall.png', ' ')
    wall_rock = surface_manager.add_icon('wall_rock', ':rock_wall.png', '#')
    stairs_down = surface_manager.add_icon('stairs_down', ':stairs_down.png', '>')
    stairs_up = surface_manager.add_icon('stairs_up', ':stairs_up.png', '<')

    room_generators = [CrimsonLairGenerator(floor_natural,
                                           wall_empty,
                                           ['crimson lair'],
                                           rng)]
    level_partitioners = [GridPartitioner(['crimson lair'],
                                           1,
                                           1,
                                           rng)]

    surrounder_config = SurroundingDecoratorConfig(['crimson lair'],
                                                   wall_natural)
    surrounder = SurroundingDecorator(surrounder_config)

    replacer_config = ReplacingDecoratorConfig(['crimson lair'],
                                    {floor_natural: floor_rock},
                                    {wall_natural: wall_ground,
                                     wall_constructed: wall_rock})
    replacer = ReplacingDecorator(replacer_config)

    wallbuilder_config = WallBuilderDecoratorConfig(['crimson lair'],
                                        {wall_natural: wall_constructed},
                                         wall_empty)
    wallbuilder = WallBuilderDecorator(wallbuilder_config)

    wall = surface_manager.add_icon('abyss_wall', ':abyss_wall.png', '#')
    wall_15 = surface_manager.add_icon('abyss_wall_15', ':abyss_wall_15.png', '#')
    wall_57 = surface_manager.add_icon('abyss_wall_57', ':abyss_wall_57.png', '#')
    wall_35 = surface_manager.add_icon('abyss_wall_35', ':abyss_wall_35.png', '#')
    wall_37 = surface_manager.add_icon('abyss_wall_37', ':abyss_wall_37.png', '#')
    wall_17 = surface_manager.add_icon('abyss_wall_17', ':abyss_wall_17.png', '#')
    wall_13 = surface_manager.add_icon('abyss_wall_13', ':abyss_wall_13.png', '#')
    wall_135 = surface_manager.add_icon('abyss_wall_135', ':abyss_wall_135.png', '#')
    wall_357 = surface_manager.add_icon('abyss_wall_357', ':abyss_wall_357.png', '#')
    wall_1357 = surface_manager.add_icon('abyss_wall_1357', ':abyss_wall_1357.png', '#')
    wall_137 = surface_manager.add_icon('abyss_wall_137', ':abyss_wall_137.png', '#')
    wall_157 = surface_manager.add_icon('abyss_wall_157', ':abyss_wall_157.png', '#')

    floor = surface_manager.add_icon('abyss_floor', ':abyss_floor.png', ' ')
    floor1 = surface_manager.add_icon('abyss_floor_1', ':abyss_floor_1.png', ' ')
    floor3 = surface_manager.add_icon('abyss_floor_3', ':abyss_floor_3.png', ' ')
    floor5 = surface_manager.add_icon('abyss_floor_5', ':abyss_floor_5.png', ' ')
    floor7 = surface_manager.add_icon('abyss_floor_7', ':abyss_floor_7.png', ' ')
    floor13 = surface_manager.add_icon('abyss_floor_13', ':abyss_floor_13.png', ' ')
    floor15 = surface_manager.add_icon('abyss_floor_15', ':abyss_floor_15.png', ' ')
    floor17 = surface_manager.add_icon('abyss_floor_17', ':abyss_floor_17.png', ' ')
    floor35 = surface_manager.add_icon('abyss_floor_35', ':abyss_floor_35.png', ' ')
    floor37 = surface_manager.add_icon('abyss_floor_37', ':abyss_floor_37.png', ' ')
    floor57 = surface_manager.add_icon('abyss_floor_57', ':abyss_floor_57.png', ' ')
    floor135 = surface_manager.add_icon('abyss_floor_135', ':abyss_floor_135.png', ' ')
    floor137 = surface_manager.add_icon('abyss_floor_137', ':abyss_floor_137.png', ' ')
    floor157 = surface_manager.add_icon('abyss_floor_157', ':abyss_floor_157.png', ' ')
    floor357 = surface_manager.add_icon('abyss_floor_357', ':abyss_floor_357.png', ' ')
    floor1357 = surface_manager.add_icon('abyss_floor_1357', ':abyss_floor_1357.png', ' ')

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

    aggregate_decorator_config = AggregateDecoratorConfig(
                                                ['crimson lair'],
                                                [surrounder,
                                                 wallbuilder,
                                                 wall_direction_builder,
                                                 floor_builder,
                                                 replacer])

    decorators = [AggregateDecorator(aggregate_decorator_config)]

    item_adder_config = ItemAdderConfiguration(['crimson lair'])
    item_adder_config.add_item(min_amount = 2,
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
    item_adders = [ItemAdder(item_generator,
                            item_adder_config,
                            rng)]

    creatures_upper = CreatureAdderConfiguration(['crimson lair'])
    creatures_upper.add_creature(min_amount = 1,
                                 max_amount = 1,
                                 name = 'crimson jaw')

    creature_adders = [CreatureAdder(creature_generator,
                                    creatures_upper,
                                    rng)]

    portal_adder_configurations = [PortalAdderConfiguration(
                                        icons = (stairs_down,
                                                 stairs_up),
                                        level_type = 'lower catacombs',
                                        location_type = 'room',
                                        chance = 10,
                                        new_level = 'crimson lair',
                                        unique = True)
                                        ]

    level_context = LevelContext(size = level_size,
                                 floor_type = 0,
                                 wall_type = wall_natural,
                                 level_types = ['crimson lair'])

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


    crimson_jaw_f0 = surface_manager.add_icon('crimson jaw_f0', ':crimson-jaw_f0.png', '&', ['bold', 'red'])
    crimson_jaw_f1 = surface_manager.add_icon('crimson jaw_f1', ':crimson-jaw_f1.png', '&', ['bold', 'red'])
    config.append(creature_config(name = 'crimson jaw',
                                  body = 12,
                                  finesse = 9,
                                  mind = 12,
                                  hp = 30,
                                  speed = 3,
                                  icons = (crimson_jaw_f0, crimson_jaw_f1),
                                  attack = 8,
                                  inventory = [inventory_config(
                                      item_name = 'whip of ashmque',
                                      min_amount = 0,
                                      max_amount = 1,
                                      probability = 100)],
                                  ai = SkeletonWarriorAI))

    return config

def init_items(context):
    """
    Initialise special items

    :returns: item configurations
    :rtype: [ItemConfiguration]
    """
    surface_manager = context.surface_manager
    config = []

    config.append(
                  ItemConfiguration(name = 'whip of ashmque',
                                    cost = 0,
                                    weight = 12,
                                    icons = [surface_manager.add_icon('whip of ashmque', ':ashmque.png', ')', ['bold', 'red'])],
                                    types = ['weapon',
                                             'one-handed',
                                             'melee',
                                             'exotic weapon'],
                                    rarity = 'artifact',
                                    effect_handles = [EffectHandle(
                                            trigger = 'on attack hit',
                                            effect = 'major fire damage',
                                            parameters = None,
                                            charges = 999999)],
                                    weapon_configration = WeaponConfiguration(
                                            damage = [(12, SLASHING_DAMAGE)],
                                            critical_range = 10,
                                            critical_damage = 12,
                                            weapon_class = 'exotic')))

    return config
