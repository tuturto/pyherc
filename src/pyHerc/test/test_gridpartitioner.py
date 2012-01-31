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
Tests for GridPartitioner
'''

from pyHerc.generators.level.partitioners.grid import GridPartitioner
from pyHerc.generators.level.partitioners.section import Section
from pyHerc.data import Level
from mock import Mock

class test_GridPartitioner:
    '''
    Tests for GridPartitioner
    '''
    def test_partitioning_returns_sections(self):
        '''
        Test that partitioning level returns default amount of sections
        '''
        mock_level = Mock(Level)
        mock_level.get_size.return_value = (20, 20)

        partitioner = GridPartitioner()
        sections = partitioner.partition_level(mock_level, 3, 3)

        assert len(sections) == 9

class test_GridPartitionerUtilities:
    '''
    Tests for various utility methods
    '''

    def test_splitting_range(self):
        '''
        Test that a line can be split into equal parts
        '''
        partitioner = GridPartitioner()

        ranges = partitioner.split_range_to_equals(10, 3)

        assert len(ranges) == 3

        assert ranges[0] == (0, 2)
        assert ranges[1] == (3, 5)
        assert ranges[2] == (6, 8)
