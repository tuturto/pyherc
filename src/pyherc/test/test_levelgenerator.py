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
Tests for LevelGenerator
"""
#pylint: disable=W0614
from pyherc.generators.level.generator import LevelGenerator
from pyherc.generators.level.generator import LevelGeneratorFactory
from pyherc.generators.level.config import LevelGeneratorFactoryConfig
from pyherc.generators.level.partitioners import GridPartitioner
from pyherc.generators.level.partitioners.section import Section
from pyherc.generators.level.room.squareroom import SquareRoomGenerator
from pyherc.generators.level.decorator import ReplacingDecorator
from pyherc.generators.level.portals import PortalAdder
from pyherc.generators.level.portals import PortalAdderConfiguration
from pyherc.generators.level.creatures import CreatureAdder
from pyherc.generators.level.items import ItemAdder
from pyherc.rules import ActionFactory
from pyherc.data import Portal
from pyherc.data import Model
from pyherc.data.tiles import FLOOR_ROCK, WALL_EMPTY
from mockito import mock, verify, when, any
from hamcrest import * #pylint: disable=W0401
from pyherc.test.matchers import map_accessibility_in
import random

class TestLeveltGeneratorFactory:
    """
    Class for testing LevelGeneratorFactory
    """
    def __init__(self):
        """
        Default constructor
        """
        self.mock_action_factory = None
        self.mock_config = None
        self.mock_partitioner = None
        self.mock_room_generator = None
        self.decorator = None
        self.mock_item_adder = None
        self.mock_creature_adder = None
        self.factory = None
        self.rng = None

    def setup(self):
        """
        Setup test case
        """
        self.mock_action_factory = mock(ActionFactory)
        self.mock_config = mock(LevelGeneratorFactoryConfig)
        self.mock_partitioner = mock()
        self.mock_partitioner.level_types = ['crypt']
        self.mock_room_generator = mock()
        self.mock_room_generator.level_types = ['crypt']
        self.decorator = mock()
        self.decorator.level_types = ['crypt']
        self.mock_item_adder = mock()
        self.mock_item_adder.level_types = ['crypt']
        self.mock_creature_adder = mock()
        self.mock_creature_adder.level_types = ['crypt']
        self.mock_portal_adder = mock()
        self.mock_portal_adder.level_types = ['crypt']
        self.rng = random.Random()

        self.mock_config.level_partitioners = [self.mock_partitioner]
        self.mock_config.room_generators = [self.mock_room_generator]
        self.mock_config.decorators = [self.decorator]
        self.mock_config.item_adders = [self.mock_item_adder]
        self.mock_config.creature_adders = [self.mock_creature_adder]
        self.mock_config.portal_adders = [self.mock_portal_adder]

        self.factory = LevelGeneratorFactory(self.mock_action_factory,
                                             mock(),
                                             self.mock_config,
                                             self.rng)

    def test_generating_level_generator(self):
        """
        Test that LevelGeneratorFactory can generate level generator
        """
        generator = self.factory.get_generator('crypt')

        assert generator != None
        assert generator.action_factory == self.mock_action_factory

class TestLevelGeneratorFactoryConfiguration:
    """
    Class for testing configuring of LevelGeneratorFactory
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def test_passing_partitioner_to_generator(self):
        """
        Test that LevelPartitioner is correctly passed to LevelGenerator
        """
        mock_action_factory = mock(ActionFactory)
        mock_partitioner = mock(GridPartitioner)
        mock_partitioner.level_types = ['crypt']
        mock_room_generator = mock()
        mock_room_generator.level_types = ['crypt']
        mock_decorator = mock()
        mock_decorator.level_types = ['crypt']
        mock_item_adder = mock()
        mock_item_adder.level_types = ['crypt']
        mock_creature_adder = mock()
        mock_creature_adder.level_types = ['crypt']
        mock_portal_adder = mock()
        mock_portal_adder.level_types = ['crypt']

        mock_config = mock(LevelGeneratorFactoryConfig)
        mock_config.level_partitioners = [mock_partitioner]
        mock_config.room_generators = [mock_room_generator]
        mock_config.decorators = [mock_decorator]
        mock_config.item_adders = [mock_item_adder]
        mock_config.creature_adders = [mock_creature_adder]
        mock_config.portal_adders = [mock_portal_adder]

        factory = LevelGeneratorFactory(mock_action_factory,
                                        mock(),
                                        mock_config,
                                        random.Random())

        generator = factory.get_generator(level_type = 'crypt')

        assert_that(generator.partitioner, is_(same_instance(mock_partitioner)))

    def test_level_type_is_checked(self):
        """
        Check that room generator with incorrect level type is not used
        """
        mock_action_factory = mock(ActionFactory)
        mock_partitioner = mock(GridPartitioner)
        mock_partitioner.level_types = ['crypt']
        mock_room_generator = mock()
        mock_room_generator.level_types = ['swamp']
        mock_decorator = mock()

        mock_config = mock(LevelGeneratorFactoryConfig)
        mock_config.level_partitioners = [mock_partitioner]
        mock_config.room_generators = [mock_room_generator]
        mock_config.decorators = [mock_decorator]
        random_generator = random.Random()

        exception_was_thrown = False

        factory = LevelGeneratorFactory(mock_action_factory,
                                        mock(),
                                        mock_config,
                                        random_generator)

        try:
            generator = factory.get_generator('crypt')
        except RuntimeError, err:
            assert_that(str(err), contains_string("No room for type crypt"))
            exception_was_thrown = True

        assert_that(exception_was_thrown)

class TestFactorySupportForLevelTypes:
    """
    Class for testing configuring of LevelGeneratorFactory with level types
    """
    def __init__(self):
        """
        Default constructor
        """
        self.partitioner_1 = None
        self.partitioner_2 = None
        self.room_generator_1 = None
        self.room_generator_2 = None
        self.decorator_1 = None
        self.decorator_2 = None
        self.item_adder_1 = None
        self.item_adder_2 = None
        self.creature_adder_1 = None
        self.creature_adder_2 = None
        mock_config = None
        self.random_generator = None
        self.factory = None

    def setup(self):
        """
        Setup test case
        """
        mock_action_factory = mock(ActionFactory)
        self.partitioner_1 = mock(GridPartitioner)
        self.partitioner_1.level_types = ['crypt', 'castle']
        self.partitioner_2 = mock(GridPartitioner)
        self.partitioner_2.level_types = ['swamp']

        self.room_generator_1 = mock(SquareRoomGenerator)
        self.room_generator_1.level_types = ['crypt']
        self.room_generator_2 = mock(SquareRoomGenerator)
        self.room_generator_2.level_types = ['swamp', 'castle']

        self.decorator_1 = mock(ReplacingDecorator)
        self.decorator_1.level_types = ['crypt', 'swamp']
        self.decorator_2 = mock(ReplacingDecorator)
        self.decorator_2.level_types = ['castle']

        self.item_adder_1 = mock(ItemAdder)
        self.item_adder_1.level_types = ['crypt']
        self.item_adder_2 = mock(ItemAdder)
        self.item_adder_2.level_types = ['castle']

        self.creature_adder_1 = mock(CreatureAdder)
        self.creature_adder_1.level_types = ['crypt', 'castle']
        self.creature_adder_2 = mock(CreatureAdder)
        self.creature_adder_2.level_types = ['swamp']

        mock_config = mock(LevelGeneratorFactoryConfig)
        mock_config.level_partitioners = [self.partitioner_1,
                                          self.partitioner_2]
        mock_config.room_generators = [self.room_generator_1,
                                       self.room_generator_2]
        mock_config.decorators = [self.decorator_1,
                                  self.decorator_2]
        mock_config.item_adders = [self.item_adder_1,
                                   self.item_adder_2]
        mock_config.creature_adders = [self.creature_adder_1,
                                       self.creature_adder_2]
        mock_config.portal_adder_configurations = []

        self.random_generator = random.Random()

        self.factory = LevelGeneratorFactory(mock_action_factory,
                                             mock(),
                                             mock_config,
                                             self.random_generator)

    def test_partitioner_type(self):
        """
        Test that partitioners can be retrieved by level types
        """
        generator = self.factory.get_generator('crypt')

        assert_that(generator.partitioner,
                    is_(same_instance(self.partitioner_1)))

    def test_room_generator_type(self):
        """
        Test that room generators can be retrieved by level types
        """
        generator = self.factory.get_generator('crypt')

        assert_that(generator.room_generator,
                    is_(same_instance(self.room_generator_1)))

    def test_decorator_type(self):
        """
        Test that decorators can be retrieved by level types
        """
        generator = self.factory.get_generator('crypt')

        assert_that(generator.decorator,
                    is_(same_instance(self.decorator_1)))

    def test_item_adder_type(self):
        """
        Test that item adders can be retrieved by level types
        """
        generator = self.factory.get_generator('crypt')

        assert_that(generator.item_adder,
                    is_(same_instance(self.item_adder_1)))

    def test_creature_adder_type(self):
        """
        Test that creature adders can be retrieved by level types
        """
        generator = self.factory.get_generator('crypt')

        assert_that(generator.creature_adder,
                    is_(same_instance(self.creature_adder_1)))

class TestLevelGenerator:
    """
    Class for testing LevelGenerator
    """
    def __init__(self):
        """
        Default constructor
        """
        self.rng = None

    def setup(self):
        """
        Setup the test case
        """
        self.rng = random.Random()

    def test_level_generation_steps(self):
        """
        Test that level generation steps are done
        """
        factory = mock()
        partitioner = mock()
        room_generator = mock()
        level_decorator = mock()
        stair_adder = mock()
        item_adder = mock()
        creature_adder = mock()
        rng = random.Random()

        portal = mock()

        section1 = mock()
        section2 = mock()

        when(partitioner).partition_level(any(),
                                          any(),
                                          any()).thenReturn([section1,
                                                        section2])

        generator = LevelGenerator(factory, partitioner, room_generator,
                                   level_decorator, [stair_adder],
                                   item_adder, creature_adder,
                                   self.rng,
                                   (60, 40))

        generator.generate_level(portal)

        verify(partitioner).partition_level(any(), any(), any())
        verify(room_generator, times = 2).generate_room(any())
        verify(level_decorator).decorate_level(any())
        verify(creature_adder).add_creatures(any())
        verify(item_adder).add_items(any())

    def test_generation_creates_connected_level(self):
        """
        Test that level generator creates a fully connected level
        """
        factory = mock(ActionFactory)
        partitioner = GridPartitioner(['crypt'],
                                      self.rng)
        room_generator = SquareRoomGenerator(FLOOR_ROCK,
                                             WALL_EMPTY,
                                             ['crypt'])
        level_decorator = mock()
        portal_adder = PortalAdder((1, 2),
                                  'crypt',
                                  mock(),
                                  self.rng)
        creature_adder = mock()
        item_adder = mock()

        portal = mock(Portal)

        generator = LevelGenerator(factory, partitioner, room_generator,
                                   level_decorator, [portal_adder],
                                   item_adder,
                                   creature_adder,
                                   self.rng,
                                   (60, 40))

        new_level = generator.generate_level(portal)

        assert_that(map_accessibility_in(new_level, WALL_EMPTY), is_(True))
