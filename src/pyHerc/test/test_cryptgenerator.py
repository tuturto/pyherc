#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
#
#   This file is part of pyHerc.
#
#   pyHerc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyHerc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyHerc.  If not, see <http://www.gnu.org/licenses/>.

'''
Tests for CryptGenerator
'''
from pyHerc.generators.level.crypt import CryptGenerator
from pyHerc.generators.level.crypt import CryptGeneratorFactory
from pyHerc.generators.level.config import LevelGeneratorConfig
from pyHerc.rules import ActionFactory

from mock import Mock

class TestCryptGenerator():
    '''
    Class for testing CryptGenerator
    '''
    pass

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

