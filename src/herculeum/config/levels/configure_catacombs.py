# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
from pyherc.generators.level.room import CatacombsGenerator
from pyherc.generators.level.partitioners import GridPartitioner

from pyherc.generators.level.decorator import ReplacingDecorator
from pyherc.generators.level.decorator import ReplacingDecoratorConfig
from pyherc.generators.level.decorator import WallBuilderDecorator
from pyherc.generators.level.decorator import WallBuilderDecoratorConfig
from pyherc.generators.level.decorator import AggregateDecorator
from pyherc.generators.level.decorator import AggregateDecoratorConfig

from pyherc.generators.level.items import ItemAdderConfiguration, ItemAdder
from pyherc.generators.level.creatures import CreatureAdderConfiguration
from pyherc.generators.level.creatures import CreatureAdder
from pyherc.generators import InventoryConfiguration
from pyherc.generators.level.portals import PortalAdderConfiguration

from pyherc.config.dsl import LevelConfiguration, LevelContext
from pyherc.generators import CreatureConfiguration
from pyherc.ai import FlockingHerbivore, SkeletonWarriorAI
from pyherc.ai.rat import RatAI
from pyherc.ai.firebeetle import FireBeetleAI
from pyherc.data.effects import DamageModifier

from pyherc.rules.constants import PIERCING_DAMAGE, CRUSHING_DAMAGE
from pyherc.rules.constants import LIGHT_DAMAGE, POISON_DAMAGE

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

    wall_empty = surface_manager.add_icon('empty wall',
                                          ':transparent.png',
                                          None)
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

    wallbuilder_config = WallBuilderDecoratorConfig(['upper catacombs',
                                                    'lower catacombs'],
                                        {wall_natural: wall_constructed},
                                        wall_empty)
    wallbuilder = WallBuilderDecorator(wallbuilder_config)

    aggregate_decorator_config = AggregateDecoratorConfig(
                                                ['upper catacombs',
                                                'lower catacombs'],
                                                [wallbuilder,
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
                                        icons = (stairs_down,
                                                 stairs_up),
                                        level_type = 'upper catacombs',
                                        location_type = 'room',
                                        chance = 100,
                                        new_level = 'lower catacombs',
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
                                 floor_type = floor_natural,
                                 wall_type = wall_natural,
                                 empty_floor = 0,
                                 empty_wall = wall_empty,
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

    config.append(CreatureConfiguration(name = 'rat',
                                        body = 4,
                                        finesse = 12,
                                        mind = 2,
                                        hp = 2,
                                        speed = 2,
                                        icons = surface_manager.add_icon(
                                                        'rat',
                                                        ':mouse.png', 
                                                        'r', 
                                                        ['yellow', 'dim']),
                                        attack = 1,
                                        ai = RatAI))

    config.append(CreatureConfiguration(name = 'fire beetle',
                                        body = 10,
                                        finesse = 11,
                                        mind = 0,
                                        hp = 4,
                                        speed = 3,
                                        icons = surface_manager.add_icon(
                                                        'fire beetle',
                                                        ':scarab-beetle.png',
                                                        'a',
                                                        ['red']),
                                        attack = 2,
                                        ai = FireBeetleAI))

    skeleton_inventory = [InventoryConfiguration(item_name = 'sword',
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

    config.append(CreatureConfiguration(name = 'skeleton warrior',
                                        body = 8,
                                        finesse = 11,
                                        mind = 0,
                                        hp = 8,
                                        speed = 4,
                                        icons = surface_manager.add_icon(
                                                        'skeleton warrior',
                                                        ':blade-bite.png',
                                                        'Z',
                                                        ['white', 'bold']),
                                        attack = 1,
                                        ai = SkeletonWarriorAI,
                                        inventory = skeleton_inventory,
                                        effects = skeleton_effects))

    return config
