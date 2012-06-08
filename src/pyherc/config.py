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
from pyherc.rules.consume.factories import DrinkFactory
from pyherc.rules.attack.factories import AttackFactory
from pyherc.rules.attack.factories import UnarmedCombatFactory
from pyherc.rules.attack.factories import MeleeCombatFactory
from pyherc.rules.inventory.factories import InventoryFactory
from pyherc.rules.inventory.factories import PickUpFactory
from pyherc.generators import ItemGenerator, CreatureGenerator
from pyherc.generators.level.portals import PortalAdderFactory
from pyherc.generators.level.portals import PortalAdderConfiguration
from pyherc.generators.level.generator import LevelGeneratorFactory
from pyherc.generators.level.config import LevelGeneratorFactoryConfig
from pyherc.generators.level.room import SquareRoomGenerator
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

from pyherc.rules.effects import EffectsFactory
from pyherc.rules.effects import Heal, Poison

from pyherc.rules.tables import Tables

from pyherc.generators.level.prototiles import FLOOR_NATURAL, FLOOR_CONSTRUCTED
from pyherc.generators.level.prototiles import WALL_EMPTY, WALL_NATURAL
from pyherc.generators.level.prototiles import WALL_CONSTRUCTED

from pyherc.data.tiles import FLOOR_ROCK, FLOOR_BRICK
from pyherc.data.tiles import WALL_EMPTY, WALL_GROUND, WALL_ROCK
from pyherc.data.tiles import PORTAL_STAIRS_UP, PORTAL_STAIRS_DOWN

class Configuration(object):
    """
    Configuration object for Herculeum
    """
    def __init__(self, base_path, model):
        """
        Default constructor

        Args:
            base_path: path to resources directory
            model: Model to register with factories
        """
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
        """
        self.resolution = (800, 600)
        self.full_screen = True
        self.caption = 'Herculeum'

        self.surface_manager = pyherc.gui.surfaceManager.SurfaceManager()
        self.surface_manager.load_resources(self.base_path)

        self.level_size = (80, 30)

        self.initialise_factories()
        self.initialise_tables()
        self.initialise_generators()
        self.initialise_level_generators()

    def initialise_factories(self):
        """
        Initialises action factory, sub factories and various generators
        """
        self.logger.info('Initialising action sub system')

        walk_factory = WalkFactory()
        move_factory = MoveFactory(walk_factory)

        effect_factory = EffectsFactory()
        effect_factory.add_effect('cure minor wounds',
                                        {'type': Heal,
                                        'duration': 20,
                                        'frequency': 5,
                                        'tick': 2,
                                        'healing': 1})
        effect_factory.add_effect('cure medium wounds',
                                        {'type': Heal,
                                        'duration': 20,
                                        'frequency': 5,
                                        'tick': 2,
                                        'healing': 2})
        effect_factory.add_effect('minor poison',
                                        {'type': Poison,
                                        'duration': 240,
                                        'frequency': 60,
                                        'tick': 60,
                                        'damage': 1})

        unarmed_combat_factory = UnarmedCombatFactory(effect_factory)
        melee_combat_factory = MeleeCombatFactory(effect_factory)
        attack_factory = AttackFactory([
                                        unarmed_combat_factory,
                                        melee_combat_factory])

        drink_factory = DrinkFactory(effect_factory)

        inventory_factory = InventoryFactory(PickUpFactory())

        self.action_factory = ActionFactory(
                                            self.model,
                                            [move_factory,
                                            attack_factory,
                                            drink_factory,
                                            inventory_factory])

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
        self.creature_generator = CreatureGenerator(self.model,
                                                    self.action_factory,
                                                    self.tables,
                                                    self.rng)

        self.logger.info('Generators initialised')

    def initialise_level_generators(self):
        """
        Initialise level generators
        """
        self.logger.info('Initialising level generators')

        config = LevelGeneratorFactoryConfig([],
                                             [],
                                             [],
                                             [],
                                             [],
                                             [],
                                             self.level_size)

        self.extend_configuration(config, self.init_catacombs())
        self.extend_configuration(config, self.init_upper_crypt())


        portal_adder_factory = PortalAdderFactory(
                                config.portal_adder_configurations,
                                self.rng)

        self.level_generator_factory = LevelGeneratorFactory(
                                                    self.action_factory,
                                                    portal_adder_factory,
                                                    config,
                                                    self.rng)

        self.logger.info('Level generators initialised')

    def extend_configuration(self, config, new_config):
        """
        Sums two configurations together

        Args:
            config: config to extend
            new_config: items to add to configuration
        """
        config.room_generators.extend(new_config.room_generators)
        config.level_partitioners.extend(new_config.level_partitioners)
        config.decorators.extend(new_config.decorators)
        config.item_adders.extend(new_config.item_adders)
        config.creature_adders.extend(new_config.creature_adders)
        config.portal_adder_configurations.extend(
                                    new_config.portal_adder_configurations)

    def init_catacombs(self):
        """
        Initialise upper catacombs
        """
        room_generators = [CatacombsGenerator(FLOOR_NATURAL,
                                               WALL_EMPTY,
                                               ['upper catacombs',
                                               'lower catacombs'],
                                               self.rng)]
        level_partitioners = [GridPartitioner(['upper catacombs',
                                               'lower catacombs'],
                                               1,
                                               1,
                                               self.rng)]

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
        item_adders = [ItemAdder(self.item_generator,
                                item_adder_config,
                                self.rng)]

        creatures_upper = CreatureAdderConfiguration(['upper catacombs'])
        creatures_upper.add_creature(min_amount = 6,
                                     max_amount = 12,
                                     name = 'rat')

        creatures_lower = CreatureAdderConfiguration(['lower catacombs'])
        creatures_lower.add_creature(min_amount = 6,
                                     max_amount = 12,
                                     name = 'rat')
        creatures_lower.add_creature(min_amount = 2,
                                     max_amount = 5,
                                     name = 'fire beetle')

        creature_adders = [CreatureAdder(self.creature_generator,
                                        creatures_upper,
                                        self.rng),
                           CreatureAdder(self.creature_generator,
                                        creatures_lower,
                                        self.rng)
                                        ]

        portal_adder_configurations = [PortalAdderConfiguration(
                                            icons = (PORTAL_STAIRS_DOWN,
                                                     PORTAL_STAIRS_UP),
                                            level_type = 'upper catacombs',
                                            location_type = 'room',
                                            chance = 100,
                                            new_level = 'lower catacombs',
                                            unique = True),
                                        PortalAdderConfiguration(
                                            icons = (PORTAL_STAIRS_DOWN,
                                                     PORTAL_STAIRS_UP),
                                            level_type = 'upper catacombs',
                                            location_type = 'room',
                                            chance = 25,
                                            new_level = 'upper crypt',
                                            unique = True)
                                            ]

        config = LevelGeneratorFactoryConfig(room_generators,
                                             level_partitioners,
                                             decorators,
                                             item_adders,
                                             creature_adders,
                                             portal_adder_configurations,
                                             self.level_size)

        return config

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
                                              4,
                                              3,
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
        item_adders = [ItemAdder(self.item_generator,
                                item_adder_config,
                                self.rng)]

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

