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

'''
Tests for CryptGenerator
'''
from pyherc.generators.level.crypt import CryptGenerator
from pyherc.generators.level.crypt import CryptGeneratorFactory
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
from pyherc.test.matchers import whole_map_is_accessible_in

import random

class TestCryptGeneratorFactory:
    '''
    Class for testing CryptGeneratorFactory
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        self.mock_action_factory = None
        self.mock_config = None
        self.mock_partitioner = None
        self.factory = None

    def setup(self):
        '''
        Setup test case
        '''
        self.mock_action_factory = stub(ActionFactory)
        self.mock_config = stub(LevelGeneratorConfig)
        self.mock_partitioner = empty_stub()

        self.factory = CryptGeneratorFactory(self.mock_action_factory,
                                             [self.mock_config])

    def test_generating_level_generator(self):
        '''
        Test that CryptGeneratorFactory can generate level generator
        '''
        generator = self.factory.get_generator(level = 1)

        assert generator != None
        assert generator.action_factory == self.mock_action_factory

class TestCryptGeneratorFactoryConfiguration:
    '''
    Class for testing configuring of CryptGeneratorFactory
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        pass

    def test_passing_partitioner_to_generator(self):
        '''
        Test that LevelPartitioner is correctly passed to CryptGenerator
        '''
        mock_action_factory = stub(ActionFactory)
        mock_partitioner = empty_stub()
        mock_config = stub(LevelGeneratorConfig)
        mock_config.level_partitioners = [mock_partitioner]

        factory = CryptGeneratorFactory(mock_action_factory,
                                             [mock_config])

        generator = factory.get_generator(level = 1)

        assert mock_partitioner in generator.level_partitioners

class TestCryptGenerator:
    '''
    Class for testing CryptGenerator
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        pass

    def test_level_generation_steps(self):
        '''
        Test that level generation steps are done
        '''
        factory = stub(ActionFactory)
        partitioner = spy(GridPartitioner)
        room_generator = spy(SquareRoomGenerator)
        level_decorator = empty_spy()
        stair_adder = empty_spy()
        config = stub(LevelGeneratorConfig)
        config.level_partitioners = [partitioner]
        config.room_generators = [room_generator]

        portal = stub(Portal)
        model = stub(Model)

        section1 = stub(Section)
        section2 = stub(Section)
        when(partitioner.partition_level).then_return([section1,
                                                       section2])

        generator = CryptGenerator(factory, config, random.Random())

        generator.generate_level(portal, model)

        assert_that_method(partitioner.partition_level).was_called()
        assert_that_method(room_generator.generate_room).was_called().times(2)
        assert_that_method(level_decorator.decorate_level).was_called()
        assert_that_method(stair_adder.add_stairs).was_called()

    def test_generation_creates_connected_level(self):
        """
        Test that crypt generator creates a fully connected level
        """
        factory = stub(ActionFactory)
        partitioner = GridPartitioner()
        room_generator = SquareRoomGenerator(floor_tile = FLOOR_ROCK,
                                             empty_tile = WALL_EMPTY)
        level_decorator = empty_spy()
        stair_adder = empty_spy()
        config = LevelGeneratorConfig()
        config.level_partitioners.append(partitioner)
        config.room_generators.append(room_generator)

        portal = stub(Portal)
        model = stub(Model)

        generator = CryptGenerator(factory, config, random.Random())

        new_level = generator.generate_level(portal, model)

        assert_that(is_(True), whole_map_is_accessible_in(new_level))
