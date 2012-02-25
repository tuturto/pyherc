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
Module for partitioning level to equal grid
"""

import random
import logging
from pyherc.generators.level.partitioners.section import Section

class RandomConnector(object):
    """
    Class for building random connection network from sections
    """
    def __init__(self, random_generator = random.Random()):
        """
        Default constructor

        Args:
            random_generator: optional random number generator
        """
        self.random_generator = random_generator
        self.logger = logging.getLogger('pyherc.generators.level.partitioners.grid.RandomConnector') #pylint: disable=C0301

    def connect_sections(self, sections, start_section = None):
        """
        Connects sections together

        Args:
            sections: List of Sections to connect
            start_section: optional parameter specifying starting section
        """
        self.logger.debug('connecting sections')

        if start_section == None:
            start_location = self.random_generator.choice(sections)
        else:
            start_location = start_section

        self.form_path_from_sections(start_location, sections)

        unconnected_sections = [x for x in sections
                                                if x.connected == False]

        while len(unconnected_sections) > 0:
            self.logger.debug('branching')
            edge_sections = [x for x in sections
                             if x.connected == True
                             and x.has_unconnected_neighbours()]

            start_location = self.random_generator.choice(edge_sections)

            self.form_path_from_sections(start_location, sections)

            unconnected_sections = [x for x in sections
                                                if x.connected == False]

        return sections

    def form_path_from_sections(self, start_section, sections):
        """
        Builds path of connected sections

        Args:
            start_section: Section to start connecting from
            sections: List of sections to connect
        """
        current_section = start_section
        unconnected_neighbours = [x for x in current_section.neighbours
                                                if x.connected == False]

        while len(unconnected_neighbours) > 0:
            next_section = self.random_generator.choice(
                                                unconnected_neighbours)

            current_section.connect_to(next_section)

            current_section = next_section
            unconnected_neighbours = [x for x in current_section.neighbours
                                                if x.connected == False]


class GridPartitioner(object):
    """
    Class for partitioning level to equal grid
    """

    def __init__(self, random_generator = random.Random()):
        """
        Default constructor

        Args:
            random_generator: optional random number generator
        """
        self.connectors = [RandomConnector()]
        self.random_generator = random_generator

    def partition_level(self, level,  x_sections = 3,  y_sections = 3):
        """
        Creates partitioning for a given level with connection points

        Args:
            level: Level to partition

        Returns
            List of connected sections
        """
        sections = []
        section_matrix = [[None for i in range(y_sections)]
                                               for j in range(x_sections)]
        size_of_level = level.get_size()

        x_sections = self.split_range_to_equals(size_of_level[0], x_sections)
        y_sections = self.split_range_to_equals(size_of_level[1], y_sections)

        for y_block in range(len(y_sections)):
            for x_block in range(len(x_sections)):
                temp_section = Section(
                                       (x_sections[x_block][0],
                                        y_sections[y_block][0]),
                                        (x_sections[x_block][1],
                                        y_sections[y_block][1]),
                                        level)

                self.connect_new_section(temp_section,
                                         (x_block, y_block),
                                         section_matrix)
                section_matrix[x_block][y_block] = temp_section
                sections.append(temp_section)

        connector = self.random_generator.choice(self.connectors)
        connected_sections = connector.connect_sections(sections)

        return connected_sections

    def connect_new_section(self, section, location, sections):
        """
        Connects section in given location to its neighbours
        """
        if location[0] > 0:
            left_section = sections[location[0]-1][location[1]]
            left_section.neighbours.append(section)
            section.neighbours.append(left_section)

        if location[1] > 0:
            up_section = sections[location[0]][location[1]-1]
            up_section.neighbours.append(section)
            section.neighbours.append(up_section)

    def split_range_to_equals(self, length, sections):
        """
        Split range into equal sized chunks

        Args:
            length: range to split
            sections: amount of sections to split

        Returns:
            list containing end points of chunks
        """
        section_length = length // sections
        ranges = []

        for i in range(sections):
            ranges.append((i * section_length, (i + 1) * section_length - 1))

        return ranges
