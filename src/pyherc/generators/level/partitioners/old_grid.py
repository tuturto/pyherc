# -*- coding: utf-8 -*-

# Copyright (c) 2010-2017 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Module for partitioning level to equal grid
"""

import logging

from pyherc.aspects import log_debug
from pyherc.generators.level.partitioners.section import (is_connected,
                                                          unconnected_neighbours,
                                                          is_unconnected_neighbours,
                                                          mark_neighbours,
                                                          connect_sections,
                                                          neighbour_sections,
                                                          is_section_in,
                                                          section_connections)
from pyherc.generators.level.partitioners.section import new_section
from pyherc.data import level_size


class RandomConnector():
    """
    Class for building random connection network from sections
    """
    @log_debug
    def __init__(self, random_generator):
        """
        Default constructor

        :param random_generator: random number generator
        :type random_generator: Random
        """
        self.random_generator = random_generator
        self.logger = logging.getLogger('pyherc.generators.level.partitioners.grid.RandomConnector')  # noqa

    @log_debug
    def connect_sections(self, sections, start_section=None):
        """
        Connects sections together

        :param sections: sections to connect
        :type sections: [Section]
        :param start_section: optional parameter specifying starting section
        :type start_section: Section
        """
        rng = self.random_generator

        if not start_section:
            current_section = rng.choice(sections)
        else:
            current_section = start_section

        path = [current_section]

        while True:
            possible_neighbours = list(unconnected_neighbours(current_section))

            while possible_neighbours:

                new_section = rng.choice(possible_neighbours)

                connect_sections(current_section, new_section)
                current_section = new_section
                path.append(current_section)

                possible_neighbours = list(unconnected_neighbours(current_section))
                
            branches = [x for x in path
                        if len(list(unconnected_neighbours(x))) > 0]

            if branches:
                current_section = rng.choice(branches)
            else:
                break

        return sections
