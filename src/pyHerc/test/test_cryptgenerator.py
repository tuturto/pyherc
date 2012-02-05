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
from pyherc.generators.level.room.squareroom import SquareRoom
from pyherc.rules import ActionFactory
from pyherc.data import Portal
from pyherc.data import Model

from mock import Mock

import random

class TestCryptGeneratorFactory:
    '''
    Class for testing CryptGeneratorFactory
    '''
    def setup(self):
        '''
        Setup test case
        '''
        self.mock_action_factory = Mock(ActionFactory)
        self.mock_config = Mock(LevelGeneratorConfig)
        self.mock_partitioner = Mock()

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
    def test_passing_partitioner_to_generator(self):
        '''
        Test that LevelPartitioner is correctly passed to CryptGenerator
        '''
        mock_action_factory = Mock(ActionFactory)
        mock_partitioner = Mock()
        mock_config = Mock(LevelGeneratorConfig)
        mock_config.level_partitioners = [mock_partitioner]

        factory = CryptGeneratorFactory(mock_action_factory,
                                             [mock_config])

        generator = factory.get_generator(level = 1)

        assert mock_partitioner in generator.level_partitioners

class TestCryptGenerator:
    '''
    Class for testing CryptGenerator
    '''
    def test_level_generation_steps(self):
        '''
        Test that level generation steps are done
        '''
        mock_factory = Mock(ActionFactory)
        mock_partitioner = Mock(GridPartitioner)
        mock_room_generator = Mock(SquareRoom)
        mock_level_decorator = Mock()
        mock_stair_adder = Mock()
        mock_config = Mock(LevelGeneratorConfig)
        mock_config.level_partitioners = [mock_partitioner]
        mock_config.room_generators = [mock_room_generator]

        mock_portal = Mock(Portal)
        mock_model = Mock(Model)

        mock_section1 = Mock(Section)
        mock_section2 = Mock(Section)
        mock_partitioner.partition_level.return_value = [mock_section1,
                                                         mock_section2]

        generator = CryptGenerator(mock_factory, mock_config, random.Random())

        generator.generate_level(mock_portal, mock_model)

        assert mock_partitioner.partition_level.called
        assert mock_room_generator.generate_room.called
        assert mock_level_decorator.decorate_level.called
        assert mock_stair_adder.add_stairs.called
