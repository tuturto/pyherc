#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
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
Configuration for herculeum
"""
import logging
import random
import pyherc.gui.surfaceManager
from pyherc.rules.public import ActionFactory
from pyherc.rules.move.factories import MoveFactory
from pyherc.rules.move.factories import WalkFactory
from pyherc.rules.attack.factories import AttackFactory
from pyherc.rules.attack.factories import UnarmedCombatFactory
from pyherc.rules.attack.factories import MeleeCombatFactory
from pyherc.generators import ItemGenerator, CreatureGenerator
from pyherc.generators.level.portals import PortalAdderFactory
from pyherc.generators.level.generator import LevelGenerator
from pyherc.generators.level.generator import LevelGeneratorFactory
from pyherc.generators.level.config import LevelGeneratorFactoryConfig
from pyherc.generators.level.room import SquareRoomGenerator
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

from pyherc.rules.tables import Tables

from pyherc.generators.level.prototiles import FLOOR_NATURAL, FLOOR_CONSTRUCTED
from pyherc.generators.level.prototiles import WALL_EMPTY, WALL_NATURAL
from pyherc.generators.level.prototiles import WALL_CONSTRUCTED

from pyherc.data.tiles import FLOOR_EMPTY, FLOOR_ROCK, FLOOR_BRICK
from pyherc.data.tiles import WALL_EMPTY, WALL_GROUND, WALL_ROCK
from pyherc.data.tiles import WALL_ROCK_DECO_1, WALL_ROCK_DECO_2

class Configuration(object):
    """
    Configuration object for Herculeum
    """
    def __init__(self, base_path, model):
        super(Configuration, self).__init__()
        self.resolution = None
        self.full_screen = None
        self.caption = None
        self.surface_manager = None
        self.action_factory = None
        self.base_path = None
        self.item_generator = None
        self.creature_generator = None
        self.level_generator_factory = None
        self.tables = None
        self.level_size = None
        self.base_path = base_path
        self.model = model
        self.rng = random.Random()
        self.logger = logging.getLogger('pyherc.config.Configuration')

    def initialise(self):
        """
        Initialises configuration

        Args:
            base_path: path to root of installation
        """
        self.resolution = (800, 600)
        self.full_screen = True
        self.caption = 'Herculeum'

        self.surface_manager = pyherc.gui.surfaceManager.SurfaceManager()
        self.surface_manager.loadResources(self.base_path)

        self.level_size = (80, 30)

        self.initialise_factories()
        self.initialise_tables()
        self.initialise_generators()
        self.initialise_level_generators()

    def initialise_factories(self):
        """
        Initialises action factory, sub factories and various generators

        Args:
            model: Model to register to the factory
        """
        self.logger.info('Initialising action sub system')

        walk_factory = WalkFactory()
        move_factory = MoveFactory(walk_factory)

        unarmed_combat_factory = UnarmedCombatFactory()
        melee_combat_factory = MeleeCombatFactory()
        attack_factory = AttackFactory([
                                        unarmed_combat_factory,
                                        melee_combat_factory])

        self.action_factory = ActionFactory(
                                            self.model,
                                            [move_factory,
                                            attack_factory])

        self.logger.info('Action sub system initialised')

    def initialise_tables(self):
        """
        Initialise tables
        """
        self.logger.info('Initialising tables')
        self.tables = Tables()
        self.tables.load_tables(self.base_path)
        self.logger.info('Tables initialised')

    def initialise_generators(self):
        """
        Initialise generators
        """
        self.logger.info('Initialising generators')

        self.item_generator = ItemGenerator(self.tables)
        self.creature_generator = CreatureGenerator(self.action_factory,
                                                    self.tables)

        self.logger.info('Generators initialised')

    def initialise_level_generators(self):
        """
        Initialise level generators
        """
        self.logger.info('Initialising level generators')

        room_generators = []
        level_partitioners = []
        decorators = []
        item_adders = []
        creature_adders = []
        portal_adder_configs = []

        upper_crypt = self.init_upper_crypt()
        room_generators.extend(upper_crypt.room_generators)
        level_partitioners.extend(upper_crypt.level_partitioners)
        decorators.extend(upper_crypt.decorators)
        item_adders.extend(upper_crypt.item_adders)
        creature_adders.extend(upper_crypt.creature_adders)
        portal_adder_configs.extend(upper_crypt.portal_adder_configurations)

        portal_adder_factory = PortalAdderFactory(portal_adder_configs,
                                                  self.rng)

        config = LevelGeneratorFactoryConfig(room_generators,
                                             level_partitioners,
                                             decorators,
                                             item_adders,
                                             creature_adders,
                                             portal_adder_configs,
                                             self.level_size)

        self.level_generator_factory = LevelGeneratorFactory(
                                                    self.action_factory,
                                                    portal_adder_factory,
                                                    config,
                                                    self.rng)

        self.logger.info('Level generators initialised')

    def init_upper_crypt(self):
        """
        Initialise upper crypt levels
        """
        room_generators = [SquareRoomGenerator(FLOOR_NATURAL,
                                               WALL_EMPTY,
                                               ['upper crypt']),
                           SquareRoomGenerator(FLOOR_CONSTRUCTED,
                                               WALL_EMPTY,
                                               ['upper crypt'])]
        level_partitioners = [GridPartitioner(['upper crypt'],
                                              self.rng)]

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
        item_adder_config.add_item(min_amount = 1,
                                   max_amount = 3,
                                   type = 'weapon',
                                   location = 'room')
        item_adder_config.add_item(min_amount = 0,
                                   max_amount = 5,
                                   type = 'potion',
                                   location = 'room')
        item_adder_config.add_item(min_amount = 0,
                                   max_amount = 5,
                                   type = 'food',
                                   location = 'room')
        item_adders = [ItemAdder(self.item_generator,
                                item_adder_config,
                                self.rng)]

        creature_adder_config = CreatureAdderConfiguration(['upper crypt'])
        #creature_adder_config.add_creature(min_amount = 3,
        #                                   max_amount = 9,
        #                                   name = 'bat')
        #creature_adder_config.add_creature(min_amount = 3,
        #                                   max_amount = 9,
        #                                   name = 'spider')
        #creature_adder_config.add_creature(min_amount = 2,
        #                                   max_amount = 6,
        #                                   name = 'skeleton',
        #                                   location = 'room')
        creature_adder_config.add_creature(min_amount = 2,
                                           max_amount = 6,
                                           name = 'rat',
                                           location = 'room')

        creature_adders = [CreatureAdder(self.creature_generator,
                                        creature_adder_config,
                                        self.rng)]

        portal_adder_configurations = []

        config = LevelGeneratorFactoryConfig(room_generators,
                                             level_partitioners,
                                             decorators,
                                             item_adders,
                                             creature_adders,
                                             portal_adder_configurations,
                                             self.level_size)

        return config

