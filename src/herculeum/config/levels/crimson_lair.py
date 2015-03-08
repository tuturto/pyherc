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
module for configuring lair of crimson jaw
"""
from herculeum.ai import SkeletonWarriorAI
from pyherc.config.dsl import LevelConfiguration, LevelContext
from pyherc.data.effects import EffectHandle
from pyherc.generators import (creature_config, inventory_config,
                               ItemConfiguration, WeaponConfiguration)
from pyherc.generators.level.decorator import (DirectionalWallDecorator,
                                               DirectionalWallDecoratorConfig,
                                               FloorBuilderDecorator,
                                               FloorBuilderDecoratorConfig,
                                               SurroundingDecorator,
                                               SurroundingDecoratorConfig,
                                               WallBuilderDecorator,
                                               WallBuilderDecoratorConfig)
from pyherc.generators.level import (item_lists, item_by_type, new_level,
                                     creature_lists, creature)
from pyherc.generators.level.partitioners import grid_partitioning
from pyherc.generators.level import PortalAdderConfiguration
from pyherc.generators.level.room import CrimsonLairGenerator
from pyherc.rules.constants import SLASHING_DAMAGE


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
