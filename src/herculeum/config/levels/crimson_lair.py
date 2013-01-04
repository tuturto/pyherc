#!/usr/bin/env python
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
module for configuring lair of crimson jaw
"""
from pyherc.generators.level.room import CrimsonLairGenerator
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

from pyherc.generators.level.prototiles import FLOOR_NATURAL
from pyherc.generators.level.prototiles import WALL_EMPTY, WALL_NATURAL
from pyherc.generators.level.prototiles import WALL_CONSTRUCTED

from herculeum.config.tiles import FLOOR_ROCK
from herculeum.config.tiles import WALL_EMPTY, WALL_GROUND, WALL_ROCK
from herculeum.config.tiles import PORTAL_STAIRS_UP, PORTAL_STAIRS_DOWN

from pyherc.generators import ItemConfiguration, WeaponConfiguration
from pyherc.data.effects import EffectHandle

from pyherc.config.dsl import LevelConfiguration
from pyherc.generators import CreatureConfiguration
from pyherc.ai import SkeletonWarriorAI

def init_level(rng, item_generator, creature_generator, level_size):
    """
    Initialise lair of crimson jaw

    :returns: level configuration
    :rtype: LevelConfiguration
    """
    room_generators = [CrimsonLairGenerator(FLOOR_NATURAL,
                                           WALL_EMPTY,
                                           ['crimson lair'],
                                           rng)]
    level_partitioners = [GridPartitioner(['crimson lair'],
                                           1,
                                           1,
                                           rng)]

    replacer_config = ReplacingDecoratorConfig(['crimson lair'],
                                    {FLOOR_NATURAL: FLOOR_ROCK},
                                    {WALL_NATURAL: WALL_GROUND,
                                    WALL_CONSTRUCTED: WALL_ROCK})
    replacer = ReplacingDecorator(replacer_config)

    wallbuilder_config = WallBuilderDecoratorConfig(['crimson lair'],
                                        {WALL_NATURAL: WALL_CONSTRUCTED},
                                        WALL_EMPTY)
    wallbuilder = WallBuilderDecorator(wallbuilder_config)

    aggregate_decorator_config = AggregateDecoratorConfig(
                                                ['crimson lair'],
                                                [wallbuilder,
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
                                        icons = (PORTAL_STAIRS_DOWN,
                                                 PORTAL_STAIRS_UP),
                                        level_type = 'lower catacombs',
                                        location_type = 'room',
                                        chance = 100,
                                        new_level = 'crimson lair',
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

def init_creatures(context):
    """
    Initialise creatures

    :returns: list of creature configurations
    :rtype: [CreatureConfiguration]
    """
    config = []
    surface_manager = context.surface_manager


    config.append(CreatureConfiguration(name = 'crimson jaw',
                                        body = 12,
                                        finesse = 9,
                                        mind = 12,
                                        hp = 30,
                                        speed = 3,
                                        icons = surface_manager.add_icon('crimson jaw',
                                                                         ':crimson-jaw.png',
                                                                         '&'),
                                        attack = 8,
                                        inventory = [InventoryConfiguration(
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
                                    icons = [surface_manager.add_icon('whip of ashmque', ':ashmque.png', ')')],
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
                                            damage = [(12, 'slashing')],
                                            critical_range = 10,
                                            critical_damage = 12,
                                            weapon_class = 'exotic')))

    return config
