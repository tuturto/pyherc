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
from pyherc.generators.level.config import LevelGeneratorConfig
from pyherc.generators.level.partitioners.grid import GridPartitioner
from pyherc.generators.level.partitioners.section import Section
from pyherc.generators.level.room.squareroom import SquareRoomGenerator
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
        self.factory = None

    def setup(self):
        """
        Setup test case
        """
        self.mock_action_factory = stub(ActionFactory)
        self.mock_config = stub(LevelGeneratorConfig)
        self.mock_partitioner = empty_stub()
        self.mock_room_generator = empty_stub()
        self.mock_room_generator.level_types = ['crypt']
        self.decorator = empty_stub()

        self.mock_config.level_partitioners = [self.mock_partitioner]
        self.mock_config.room_generators = [self.mock_room_generator]
        self.mock_config.decorators = [self.decorator]

        self.factory = LevelGeneratorFactory(self.mock_action_factory,
                                             self.mock_config)

    def test_generating_level_generator(self):
        """
        Test that LevelGeneratorFactory can generate level generator
        """
        generator = self.factory.get_generator(level = 1,
                                            level_type = "crypt",
                                            random_generator = random.Random())

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
        mock_room_generator = empty_stub()
        mock_room_generator.level_types = ['crypt']
        mock_decorator = empty_stub()

        mock_config = stub(LevelGeneratorConfig)
        mock_config.level_partitioners = [mock_partitioner]
        mock_config.room_generators = [mock_room_generator]
        mock_config.decorators = [mock_decorator]

        factory = LevelGeneratorFactory(mock_action_factory,
                                             mock_config)

        generator = factory.get_generator(level = 1,
                                          level_type = "crypt",
                                          random_generator = random.Random())

        assert_that(generator.partitioner, is_(same_instance(mock_partitioner)))

    def test_level_type_is_checked(self):
        """
        Check that room generator with incorrect level type is not used
        """
        mock_action_factory = stub(ActionFactory)
        mock_partitioner = stub(GridPartitioner)
        mock_room_generator = empty_stub()
        mock_room_generator.level_types = ["swamp"]
        mock_decorator = empty_stub()

        mock_config = stub(LevelGeneratorConfig)
        mock_config.level_partitioners = [mock_partitioner]
        mock_config.room_generators = [mock_room_generator]
        mock_config.decorators = [mock_decorator]

        factory = LevelGeneratorFactory(mock_action_factory,
                                             mock_config)

        generator = factory.get_generator(level = 1,
                                          level_type = "crypt",
                                          random_generator = random.Random())

        assert_that(generator.room_generator, is_(none()))

class TestLevelGenerator:
    """
    Class for testing LevelGenerator
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def test_level_generation_steps(self):
        """
        Test that level generation steps are done
        """
        factory = stub(ActionFactory)
        partitioner = spy(GridPartitioner)
        room_generator = spy(SquareRoomGenerator)
        level_decorator = empty_spy()
        stair_adder = empty_spy()

        portal = stub(Portal)
        model = stub(Model)

        section1 = stub(Section)
        section2 = stub(Section)
        when(partitioner.partition_level).then_return([section1,
                                                       section2])

        generator = LevelGenerator(factory, partitioner, room_generator, None,
                                   random.Random())

        generator.generate_level(portal, model)

        assert_that_method(partitioner.partition_level).was_called()
        assert_that_method(room_generator.generate_room).was_called().times(2)
        assert_that_method(level_decorator.decorate_level).was_called()
        assert_that_method(stair_adder.add_stairs).was_called()

    def test_generation_creates_connected_level(self):
        """
        Test that level generator creates a fully connected level
        """
        factory = stub(ActionFactory)
        partitioner = GridPartitioner()
        room_generator = SquareRoomGenerator(floor_tile = FLOOR_ROCK,
                                             empty_tile = WALL_EMPTY)
        level_decorator = empty_spy()
        stair_adder = empty_spy()

        portal = stub(Portal)
        model = stub(Model)

        generator = LevelGenerator(factory, partitioner, room_generator, None,
                                   random.Random())

        new_level = generator.generate_level(portal, model)

        assert_that(map_accessibility_in(new_level, WALL_EMPTY), is_(True))
