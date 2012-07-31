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
module for configuring upper crypt
"""
from pyherc.generators.level.partitioners import GridPartitioner
from pyherc.generators.level.room import SquareRoomGenerator

from pyherc.generators.level.decorator import ReplacingDecorator
from pyherc.generators.level.decorator import ReplacingDecoratorConfig
from pyherc.generators.level.decorator import WallBuilderDecorator
from pyherc.generators.level.decorator import WallBuilderDecoratorConfig
from pyherc.generators.level.decorator import AggregateDecorator
from pyherc.generators.level.decorator import AggregateDecoratorConfig

from pyherc.generators.level.items import ItemAdderConfiguration, ItemAdder
from pyherc.generators.level.creatures import CreatureAdderConfiguration
from pyherc.generators.level.creatures import CreatureAdder

from pyherc.generators.level.portals import PortalAdderConfiguration

from pyherc.generators.level.prototiles import FLOOR_NATURAL, FLOOR_CONSTRUCTED
from pyherc.generators.level.prototiles import WALL_EMPTY, WALL_NATURAL
from pyherc.generators.level.prototiles import WALL_CONSTRUCTED

from herculeum.config.tiles import FLOOR_ROCK, FLOOR_BRICK
from herculeum.config.tiles import WALL_EMPTY, WALL_GROUND, WALL_ROCK
from herculeum.config.tiles import PORTAL_STAIRS_UP, PORTAL_STAIRS_DOWN
from herculeum.config.tiles import CREATURE_SPIDER_1

from pyherc.ai import FlockingHerbivore
from pyherc.generators import CreatureConfiguration
from pyherc.rules.effects import EffectHandle

from pyherc.config.dsl import LevelConfiguration

def init_level(rng, item_generator, creature_generator, level_size):
    """
    Initialise upper crypt levels

    :returns: level configuration
    :rtype: LevelConfiguration
    """
    room_generators = [SquareRoomGenerator(FLOOR_NATURAL,
                                           WALL_EMPTY,
                                           ['upper crypt']),
                       SquareRoomGenerator(FLOOR_CONSTRUCTED,
                                           WALL_EMPTY,
                                           ['upper crypt'])]
    level_partitioners = [GridPartitioner(['upper crypt'],
                                          4,
                                          3,
                                          rng)]

    replacer_config = ReplacingDecoratorConfig(['upper crypt'],
                                    {FLOOR_NATURAL: FLOOR_ROCK,
                                    FLOOR_CONSTRUCTED: FLOOR_BRICK},
                                    {WALL_NATURAL: WALL_GROUND,
                                    WALL_CONSTRUCTED: WALL_ROCK})
    replacer = ReplacingDecorator(replacer_config)

    wallbuilder_config = WallBuilderDecoratorConfig(['upper crypt'],
                                        {WALL_NATURAL: WALL_CONSTRUCTED},
                                        WALL_EMPTY)
    wallbuilder = WallBuilderDecorator(wallbuilder_config)

    aggregate_decorator_config = AggregateDecoratorConfig(['upper crypt'],
                                                          [wallbuilder,
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
    item_adders = [ItemAdder(item_generator,
                            item_adder_config,
                            rng)]

    creature_adder_config = CreatureAdderConfiguration(['upper crypt'])
    #creature_adder_config.add_creature(min_amount = 6,
    #                                   max_amount = 12,
    #                                   name = 'bat')
    creature_adder_config.add_creature(min_amount = 4,
                                       max_amount = 8,
                                       name = 'spider')
    #creature_adder_config.add_creature(min_amount = 4,
    #                                   max_amount = 8,
    #                                   name = 'skeleton',
    #                                   location = 'room')

    creature_adders = [CreatureAdder(creature_generator,
                                    creature_adder_config,
                                    rng)]

    portal_adder_configurations = [PortalAdderConfiguration(
                                        icons = (PORTAL_STAIRS_DOWN,
                                                 PORTAL_STAIRS_UP),
                                        level_type = 'upper catacombs',
                                        location_type = 'room',
                                        chance = 25,
                                        new_level = 'upper crypt',
                                        unique = True)]

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
    Initialise creatures

    :returns: list of creature configurations
    :rtype: [CreatureConfiguration]
    """

    config = []

    config.append(CreatureConfiguration(name = 'spider',
                                        body = 6,
                                        finesse = 12,
                                        mind = 8,
                                        hp = 6,
                                        speed = 1,
                                        icons = CREATURE_SPIDER_1,
                                        attack = 4,
                                        ai = FlockingHerbivore,
                                        effect_handles = [EffectHandle(
                                                    trigger = 'on attack hit',
                                                    effect = 'minor poison',
                                                    parameters = None,
                                                    charges = 100)]))

    return config
