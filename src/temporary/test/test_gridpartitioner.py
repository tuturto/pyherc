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
Tests for GridPartitioner
'''

from pyherc.generators.level.partitioners.grid import GridPartitioner
from pyherc.generators.level.partitioners.grid import RandomConnector
from pyherc.generators.level.partitioners.section import Section
from pyherc.data import Level
from mock import Mock

class test_GridPartitioner:
    '''
    Tests for GridPartitioner
    '''
    def setup(self):
        '''
        Setup tests
        '''
        self.mock_level = Mock(Level)
        self.mock_level.get_size.return_value = (20, 20)

        self.partitioner = GridPartitioner()

    def test_partitioning_returns_sections(self):
        '''
        Test that partitioning level returns default amount of sections
        '''
        sections = self.partitioner.partition_level(self.mock_level, 3, 3)

        assert len(sections) == 9

    def test_sections_have_neighbours(self):
        '''
        Test that sections are marked being neighbours
        '''
        sections = self.partitioner.partition_level(self.mock_level, 2, 1)

        assert len(sections[0].neighbours) == 1

    def test_partitioned_sections_are_linked(self):
        '''
        Partitioned sections should be linked together
        '''
        sections = self.partitioner.partition_level(self.mock_level, 2, 2)

        assert len(sections) == 4

        assert len(sections[0].connections) > 0

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

class test_RandomConnector:
    '''
    Tests for RandomConnector class
    '''
    def setup(self):
        '''
        Setup the test cases
        '''
        self.connector = RandomConnector()

    def test_connect_two_sections(self):
        '''
        Test that two adjacent sections can be connected
        '''
        section1 = Section(())
        section2 = Section(())

        section1.neighbours.append(section2)
        section2.neighbours.append(section1)

        sections = [section1, section2]

        connected_sections = self.connector.connect_sections(sections)

        assert connected_sections[1] in connected_sections[0].connections

    def test_connecting_2x2_grid(self):
        '''
        Test that 2x2 grid is fully connected
        '''
        section00 = Section(())
        section10 = Section(())
        section01 = Section(())
        section11 = Section(())

        section00.neighbours.append(section10)
        section00.neighbours.append(section01)
        section10.neighbours.append(section00)
        section10.neighbours.append(section11)
        section01.neighbours.append(section00)
        section01.neighbours.append(section11)
        section11.neighbours.append(section10)
        section11.neighbours.append(section01)

        sections = [section00, section10, section01, section11]

        connected_sections = self.connector.connect_sections(sections)

        assert len(connected_sections) == 4

        for section in connected_sections:
            assert len(section.connections) > 0
            assert section.connected == True

    def test_connect_row_of_sections(self):
        '''
        Test special case where connections have to branch

        Row of Sections is connected, starting from the middle
        RandomConnector can not connect this in one path, but has to branch
        '''
        section0 = Section(())
        section1 = Section(())
        section2 = Section(())
        section3 = Section(())
        section4 = Section(())

        section0.neighbours.append(section1)
        section1.neighbours.append(section0)
        section1.neighbours.append(section2)
        section2.neighbours.append(section1)
        section2.neighbours.append(section3)
        section3.neighbours.append(section2)
        section3.neighbours.append(section4)
        section4.neighbours.append(section3)

        sections = [section0, section1, section2, section3, section4]

        connected_sections = self.connector.connect_sections(sections, section2)

        for section in connected_sections:
            assert len(section.connections) > 0
            assert section.connected == True
