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
Module for partitioning level to equal grid
'''

import random
from pyHerc.generators.level.partitioners.section import Section

class RandomConnector(object):
    '''
    Class for building random connection network from sections
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        pass

    def connect_sections(self, sections):
        '''
        Connects sections together
        @param sections: List of Sections to connect
        '''
        return sections

class GridPartitioner(object):
    '''
    Class for partitioning level to equal grid
    '''

    def __init__(self, random_generator = random.Random()):
        '''
        Default constructor
        @param random_generator: optional random number generator
        '''
        self.connectors = [RandomConnector()]
        self.random_generator = random_generator

    def partition_level(self, level,  x_sections = 3,  y_sections = 3):
        '''
        Creates partitioning for a given level with connection points
        @param level: Level to partition
        '''
        sections = []
        size_of_level = level.get_size()

        x_sections = self.split_range_to_equals(size_of_level[0], x_sections)
        y_sections = self.split_range_to_equals(size_of_level[1], y_sections)

        for y_block in range(len(y_sections)):
            for x_block in range(len(x_sections)):
                temp_section = Section((x_sections[x_block],
                                                    y_sections[y_block]))
                sections.append(temp_section)

        connector = self.random_generator.choice(self.connectors)
        connected_sections = connector.connect_sections(sections)

        return connected_sections

    def split_range_to_equals(self, length, sections):
        '''
        Split range into equal sized chunks
        @param length: range to split
        @param sections: amount of sections to split
        @returns: list containing end points of chunks
        '''
        section_length = length // sections
        ranges = []

        for i in range(sections):
            ranges.append((i * section_length, (i + 1) * section_length - 1))

        return ranges
