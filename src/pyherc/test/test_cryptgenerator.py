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
from pyDoubles.framework import stub,  empty_stub, method_returning #pylint: disable=F0401, E0611
from pyDoubles.framework import spy, assert_that_method, when, empty_spy #pylint: disable=F0401, E0611

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
        mock_factory = stub(ActionFactory)
        mock_partitioner = spy(GridPartitioner)
        mock_room_generator = spy(SquareRoomGenerator)
        mock_level_decorator = empty_spy()
        mock_stair_adder = empty_spy()
        mock_config = stub(LevelGeneratorConfig)
        mock_config.level_partitioners = [mock_partitioner]
        mock_config.room_generators = [mock_room_generator]

        mock_portal = stub(Portal)
        mock_model = stub(Model)

        mock_section1 = stub(Section)
        mock_section2 = stub(Section)
        when(mock_partitioner.partition_level).then_return([mock_section1,
                                                                mock_section2])

        generator = CryptGenerator(mock_factory, mock_config, random.Random())

        generator.generate_level(mock_portal, mock_model)

        assert_that_method(mock_partitioner.partition_level).was_called()
        assert_that_method(mock_room_generator.generate_room).was_called().times(2)
        assert_that_method(mock_level_decorator.decorate_level).was_called()
        assert_that_method(mock_stair_adder.add_stairs).was_called()
