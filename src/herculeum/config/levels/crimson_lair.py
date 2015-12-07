# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
