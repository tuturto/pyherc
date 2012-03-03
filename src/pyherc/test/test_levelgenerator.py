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
from pyDoubles.framework import stub,  empty_stub, method_returning #pylint: disable=F0401, E0611
from pyDoubles.framework import spy, assert_that_method, when, empty_spy #pylint: disable=F0401, E0611
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
        self.mock_action_factory = stub(ActionFactory)
        self.mock_config = stub(LevelGeneratorFactoryConfig)
        self.mock_partitioner = empty_stub()
        self.mock_partitioner.level_types = ['crypt']
        self.mock_room_generator = empty_stub()
        self.mock_room_generator.level_types = ['crypt']
        self.decorator = empty_stub()
        self.decorator.level_types = ['crypt']
        self.mock_item_adder = empty_stub()
        self.mock_item_adder.level_types = ['crypt']
        self.mock_creature_adder = empty_stub()
        self.mock_creature_adder.level_types = ['crypt']
        self.mock_portal_adder = empty_stub()
        self.mock_portal_adder.level_types = ['crypt']
        self.rng = random.Random()

        self.mock_config.level_partitioners = [self.mock_partitioner]
        self.mock_config.room_generators = [self.mock_room_generator]
        self.mock_config.decorators = [self.decorator]
        self.mock_config.item_adders = [self.mock_item_adder]
        self.mock_config.creature_adders = [self.mock_creature_adder]
        self.mock_config.portal_adders = [self.mock_portal_adder]

        self.factory = LevelGeneratorFactory(self.mock_action_factory,
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
        mock_action_factory = stub(ActionFactory)
        mock_partitioner = stub(GridPartitioner)
        mock_partitioner.level_types = ['crypt']
        mock_room_generator = empty_stub()
        mock_room_generator.level_types = ['crypt']
        mock_decorator = empty_stub()
        mock_decorator.level_types = ['crypt']
        mock_item_adder = empty_stub()
        mock_item_adder.level_types = ['crypt']
        mock_creature_adder = empty_stub()
        mock_creature_adder.level_types = ['crypt']
        mock_portal_adder = empty_stub()
        mock_portal_adder.level_types = ['crypt']

        mock_config = stub(LevelGeneratorFactoryConfig)
        mock_config.level_partitioners = [mock_partitioner]
        mock_config.room_generators = [mock_room_generator]
        mock_config.decorators = [mock_decorator]
        mock_config.item_adders = [mock_item_adder]
        mock_config.creature_adders = [mock_creature_adder]
        mock_config.portal_adders = [mock_portal_adder]

        factory = LevelGeneratorFactory(mock_action_factory,
                                             mock_config,
                                             random.Random())

        generator = factory.get_generator(level_type = 'crypt')

        assert_that(generator.partitioner, is_(same_instance(mock_partitioner)))

    def test_level_type_is_checked(self):
        """
        Check that room generator with incorrect level type is not used
        """
        mock_action_factory = stub(ActionFactory)
        mock_partitioner = stub(GridPartitioner)
        mock_partitioner.level_types = ['crypt']
        mock_room_generator = empty_stub()
        mock_room_generator.level_types = ['swamp']
        mock_decorator = empty_stub()

        mock_config = stub(LevelGeneratorFactoryConfig)
        mock_config.level_partitioners = [mock_partitioner]
        mock_config.room_generators = [mock_room_generator]
        mock_config.decorators = [mock_decorator]
        random_generator = random.Random()

        exception_was_thrown = False

        factory = LevelGeneratorFactory(mock_action_factory,
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
        self.portal_adder_1 = None
        self.portal_adder_2 = None
        mock_config = None
        self.random_generator = None
        self.factory = None

    def setup(self):
        """
        Setup test case
        """
        mock_action_factory = stub(ActionFactory)
        self.partitioner_1 = stub(GridPartitioner)
        self.partitioner_1.level_types = ['crypt', 'castle']
        self.partitioner_2 = stub(GridPartitioner)
        self.partitioner_2.level_types = ['swamp']

        self.room_generator_1 = stub(SquareRoomGenerator)
        self.room_generator_1.level_types = ['crypt']
        self.room_generator_2 = stub(SquareRoomGenerator)
        self.room_generator_2.level_types = ['swamp', 'castle']

        self.decorator_1 = stub(ReplacingDecorator)
        self.decorator_1.level_types = ['crypt', 'swamp']
        self.decorator_2 = stub(ReplacingDecorator)
        self.decorator_2.level_types = ['castle']

        self.item_adder_1 = stub(ItemAdder)
        self.item_adder_1.level_types = ['crypt']
        self.item_adder_2 = stub(ItemAdder)
        self.item_adder_2.level_types = ['castle']

        self.creature_adder_1 = stub(CreatureAdder)
        self.creature_adder_1.level_types = ['crypt', 'castle']
        self.creature_adder_2 = stub(CreatureAdder)
        self.creature_adder_2.level_types = ['swamp']

        self.portal_adder_1 = stub(PortalAdder)
        self.portal_adder_1.level_types = ['crypt', 'castle']
        self.portal_adder_2 = stub(PortalAdder)
        self.portal_adder_2.level_types = ['swamp']

        mock_config = stub(LevelGeneratorFactoryConfig)
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
        mock_config.portal_adders = [self.portal_adder_1,
                                     self.portal_adder_2]

        self.random_generator = random.Random()

        self.factory = LevelGeneratorFactory(mock_action_factory,
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

    def test_portal_adder_type(self):
        """
        Test that portal adders can be selected by level types
        """
        generator = self.factory.get_generator('crypt')

        assert_that(generator.portal_adders,
                    has_item(self.portal_adder_1))

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
        factory = stub(ActionFactory)
        partitioner = spy(GridPartitioner)
        room_generator = spy(SquareRoomGenerator)
        level_decorator = spy(ReplacingDecorator)
        stair_adder = spy(PortalAdder)
        item_adder = spy(ItemAdder)
        creature_adder = spy(CreatureAdder)
        rng = random.Random()

        portal = stub(Portal)

        section1 = stub(Section)
        section2 = stub(Section)
        when(partitioner.partition_level).then_return([section1,
                                                       section2])

        generator = LevelGenerator(factory, partitioner, room_generator,
                                   level_decorator, [stair_adder],
                                   item_adder, creature_adder,
                                   self.rng,
                                   (60, 40))

        generator.generate_level(portal)

        assert_that_method(partitioner.partition_level).was_called()
        assert_that_method(room_generator.generate_room).was_called().times(2)
        assert_that_method(level_decorator.decorate_level).was_called()
        assert_that_method(creature_adder.add_creatures).was_called()
        assert_that_method(item_adder.add_items).was_called()

    def test_generation_creates_connected_level(self):
        """
        Test that level generator creates a fully connected level
        """
        factory = stub(ActionFactory)
        partitioner = GridPartitioner(['crypt'],
                                      self.rng)
        room_generator = SquareRoomGenerator(FLOOR_ROCK,
                                             WALL_EMPTY,
                                             ['crypt'])
        level_decorator = empty_spy()
        stair_adder = PortalAdder('crypt',
                                  empty_stub(),
                                  self.rng)
        creature_adder = empty_spy()
        item_adder = empty_spy()

        portal = stub(Portal)

        generator = LevelGenerator(factory, partitioner, room_generator,
                                   level_decorator, [stair_adder],
                                   item_adder,
                                   creature_adder,
                                   self.rng,
                                   (60, 40))

        new_level = generator.generate_level(portal)

        assert_that(map_accessibility_in(new_level, WALL_EMPTY), is_(True))
