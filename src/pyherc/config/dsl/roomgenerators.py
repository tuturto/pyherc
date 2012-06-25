#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
module for RoomGenerators
"""
from pyherc.generators.level.room.catacombs import CatacombsGenerator

class Catacombs(object):
    """
    Generator for catacombs
    """
    def __init__(self):
        super(Catacombs, self).__init__()

    def with_(self, parameter):
        return self

    def located_at(self, location):
        return self

    def using(self, rng):
        return self

    def build(self):
        return CatacombsGenerator(floor_tile = None,
                                  empty_tile = None,
                                  level_types = [],
                                  rng = None)

def natural_floor():
    return 10, 10
