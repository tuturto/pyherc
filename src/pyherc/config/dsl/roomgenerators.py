# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
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
module for RoomGenerators
"""
from random import Random

from pyherc.generators.level.prototiles import FLOOR_NATURAL
from pyherc.generators.level.room.catacombs import CatacombsGenerator


class Catacombs():
    """
    Generator for catacombs
    """
    def __init__(self):
        """
        Default constructor
        """
        super(Catacombs, self).__init__()
        self.floor_tile = 0
        self.empty_tile = 0
        self.rng = Random()
        self.locations = []

    def with_(self, parameter):
        """
        set parameter for room generation

        :param parameter: parameter to set
        :type parameter: (string, value)
        """
        if hasattr(parameter, 'count'):
            if parameter[0] == 'floor':
                self.floor_tile = parameter[1]

        elif hasattr(parameter, 'random'):
            self.rng = parameter

        return self

    def located_at(self, location):
        """
        Set location of room

        :param location: name of location
        :type location: string
        """
        self.locations.append(location)
        return self

    def build(self):
        """
        Build generator

        :returns: configured generator
        :rtype: CatacombsGenerator
        """
        return CatacombsGenerator(floor_tile=self.floor_tile,
                                  empty_tile=self.empty_tile,
                                  level_types=self.locations,
                                  rng=self.rng)


def natural_floor():
    """
    Get definition of natural floor

    :returns: definition of natural floor
    :rtype: (string, int)
    """
    return ('floor', FLOOR_NATURAL)
