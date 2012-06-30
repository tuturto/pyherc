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
Module for testing dungeon
"""

from pyherc.data import Level
from pyherc.data import Portal

class TestDungeon:
    """
    Tests for Dungeon class
    """
    def __init__(self):
        """
        Default constructor
        """
        self.floor_rock = 1
        self.wall_empty = 2

    def test_simple_level_creation(self):
        """
        Test that simple level creation works
        """
        level = Level([20, 20], self.floor_rock, self.wall_empty)
        assert not (level is None)
        assert(level.floor[5][5] == self.floor_rock)
        assert(level.walls[0][0] == self.wall_empty)

    def test_stair_linking(self):
        """
        Test that stairs can be linked
        """
        level1 = Level([20, 20], self.floor_rock, self.wall_empty)
        level2 = Level([20, 20], self.floor_rock, self.wall_empty)

        stairs1 = Portal((None, None), None)
        #TODO: beak link
        stairs1.icon = 200
        level1.add_portal(stairs1, (10, 10))

        stairs2 = Portal((None, None), None)
        level2.add_portal(stairs2, (5, 5), stairs1)

        assert(stairs1.level == level1)
        assert(stairs1.location == (10, 10))
        assert(stairs1.other_end == stairs2)

        assert(stairs2.level == level2)
        assert(stairs2.location == (5, 5))
        assert(stairs2.other_end == stairs1)

        assert(stairs1 in level1.portals)
        assert(stairs2 in level2.portals)
