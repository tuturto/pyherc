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
module for configuring upper crypt
"""
from herculeum.ai import FlockingHerbivore
from pyherc.config.dsl import LevelConfiguration, LevelContext
from pyherc.data.effects import EffectHandle
from pyherc.data.traps import PitTrap
from pyherc.generators import creature_config
from pyherc.generators.level.decorator import (DirectionalWallDecorator,
                                               DirectionalWallDecoratorConfig,
                                               FloorBuilderDecorator,
                                               FloorBuilderDecoratorConfig,
                                               SurroundingDecorator,
                                               SurroundingDecoratorConfig,
                                               WallBuilderDecorator,
                                               WallBuilderDecoratorConfig,
                                               WallOrnamentDecorator,
                                               WallOrnamentDecoratorConfig)
from pyherc.generators.level import (ItemAdder, item_by_type, item_by_name,
                                     new_level, item_lists, creature_lists,
                                     creature)
from pyherc.generators.level.partitioners import grid_partitioning
from pyherc.generators.level import PortalAdderConfiguration
from pyherc.generators.level.room import (PillarRoomGenerator,
                                          SquareRoomGenerator)
from herculeum.config.room_generators import (circular_pitroom, square_pitroom,
                                              square_room)
from herculeum.config.floor_builders import floor_builder, pit_builder


def init_creatures(context):
    """
    Initialise creatures

    :returns: list of creature configurations
    :rtype: [CreatureConfiguration]
    """
    config = []
    surface_manager = context.surface_manager

    spider_f0 = surface_manager.add_icon('spider_f0', ':masked-spider_f0.png', 's', ['white', 'dim'])
    spider_f1 = surface_manager.add_icon('spider_f1', ':masked-spider_f1.png', 's', ['white', 'dim'])
    config.append(creature_config(name = 'spider',
                                  body = 6,
                                  finesse = 12,
                                  mind = 8,
                                  hp = 6,
                                  speed = 1,
                                  icons = (spider_f0, spider_f1),
                                  attack = 4,
                                  ai = FlockingHerbivore,
                                  effect_handles = [EffectHandle(
                                      trigger = 'on attack hit',
                                      effect = 'minor poison',
                                      parameters = None,
                                      charges = 100)]))

    return config
