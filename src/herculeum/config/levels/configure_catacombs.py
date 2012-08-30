#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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

from pyherc.generators.level.prototiles import FLOOR_NATURAL, FLOOR_CONSTRUCTED
from pyherc.generators.level.prototiles import WALL_EMPTY, WALL_NATURAL
from pyherc.generators.level.prototiles import WALL_CONSTRUCTED

from herculeum.config.tiles import FLOOR_ROCK, FLOOR_BRICK
from herculeum.config.tiles import WALL_EMPTY, WALL_GROUND, WALL_ROCK
from herculeum.config.tiles import PORTAL_STAIRS_UP, PORTAL_STAIRS_DOWN

from herculeum.config.tiles import CREATURE_RAT_1, CREATURE_RAT_2
from herculeum.config.tiles import CREATURE_RAT_3, CREATURE_RAT_4
from herculeum.config.tiles import CREATURE_BEETLE_1, CREATURE_BEETLE_2
from herculeum.config.tiles import CREATURE_SKELETON_WARRIOR

from pyherc.config.dsl import LevelConfiguration
from pyherc.generators import CreatureConfiguration
from pyherc.ai import FlockingHerbivore

def init_level(rng, item_generator, creature_generator, level_size):
    """
    Initialise upper catacombs

    :returns: level configuration
    :rtype: LevelConfiguration
    """
    room_generators = [CatacombsGenerator(FLOOR_NATURAL,
                                           WALL_EMPTY,
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
                                    {FLOOR_NATURAL: FLOOR_ROCK},
                                    {WALL_NATURAL: WALL_GROUND,
                                    WALL_CONSTRUCTED: WALL_ROCK})
    replacer = ReplacingDecorator(replacer_config)

    wallbuilder_config = WallBuilderDecoratorConfig(['upper catacombs',
                                                    'lower catacombs'],
                                        {WALL_NATURAL: WALL_CONSTRUCTED},
                                        WALL_EMPTY)
    wallbuilder = WallBuilderDecorator(wallbuilder_config)

    aggregate_decorator_config = AggregateDecoratorConfig(
                                                ['upper catacombs',
                                                'lower catacombs'],
                                                [wallbuilder,
                                                replacer])

    decorators = [AggregateDecorator(aggregate_decorator_config)]

    item_adder_config = ItemAdderConfiguration(['upper catacombs',
                                               'lower catacombs'])
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
                                        icons = (PORTAL_STAIRS_DOWN,
                                                 PORTAL_STAIRS_UP),
                                        level_type = 'upper catacombs',
                                        location_type = 'room',
                                        chance = 100,
                                        new_level = 'lower catacombs',
                                        unique = True)
                                        ]

    config = (LevelConfiguration()
                    .with_rooms(room_generators)
                    .with_partitioners(level_partitioners)
                    .with_decorators(decorators)
                    .with_items(item_adders)
                    .with_creatures(creature_adders)
                    .with_portals(portal_adder_configurations)
                    .with_level_size(level_size)
                    .build())

    return config

def init_creatures():
    """
    Initialise creatures''

    :returns: list of configuration items
    :rtype: [CreatureConfiguration]
    """

    config = []

    config.append(CreatureConfiguration(name = 'rat',
                                        body = 4,
                                        finesse = 12,
                                        mind = 2,
                                        hp = 2,
                                        speed = 2,
                                        icons = CREATURE_RAT_1,
                                        attack = 2,
                                        ai = FlockingHerbivore))

    config.append(CreatureConfiguration(name = 'fire beetle',
                                        body = 10,
                                        finesse = 11,
                                        mind = 0,
                                        hp = 4,
                                        speed = 1.9,
                                        icons = CREATURE_BEETLE_1,
                                        attack = 4,
                                        ai = FlockingHerbivore))

    skeleton_inventory = [InventoryConfiguration(item_name = 'dagger',
                                                min_amount = 0,
                                                max_amount = 1,
                                                probability = 50)]

    config.append(CreatureConfiguration(name = 'skeleton warrior',
                                        body = 8,
                                        finesse = 11,
                                        mind = 0,
                                        hp = 8,
                                        speed = 2.5,
                                        icons = CREATURE_SKELETON_WARRIOR,
                                        attack = 2,
                                        ai = FlockingHerbivore,
                                        inventory = skeleton_inventory))

    return config
