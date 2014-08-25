# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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
