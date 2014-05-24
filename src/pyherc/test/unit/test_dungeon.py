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
Module for testing dungeon
"""

from mockito import mock
from pyherc.data import Level, Portal, floor_tile, wall_tile, add_portal
from pyherc.data import get_portal


class TestDungeon:
    """
    Tests for Dungeon class
    """
    def __init__(self):
        """
        Default constructor
        """
        self.floor_rock = 1
        self.wall_empty = None

    def test_simple_level_creation(self):
        """
        Test that simple level creation works
        """
        level = Level(mock(), [20, 20], self.floor_rock, self.wall_empty)
        assert not (level is None)
        assert(floor_tile(level, (5, 5)) == self.floor_rock)
        assert(wall_tile(level, (0, 0)) == self.wall_empty)

    def test_stair_linking(self):
        """
        Test that stairs can be linked
        """
        level1 = Level(mock(), [20, 20], self.floor_rock, self.wall_empty)
        level2 = Level(mock(), [20, 20], self.floor_rock, self.wall_empty)

        stairs1 = Portal((None, None), None)

        stairs1.icon = 'stairs'
        add_portal(level1, (10, 10), stairs1)

        stairs2 = Portal((None, None), None)
        add_portal(level2, (5, 5), stairs2, stairs1)

        assert(stairs1.level == level1)
        assert(stairs1.location == (10, 10))
        assert(stairs1.get_other_end(mock()) == stairs2)

        assert(stairs2.level == level2)
        assert(stairs2.location == (5, 5))
        assert(stairs2.get_other_end(mock()) == stairs1)

        assert get_portal(level1, (10, 10)) == stairs1
        assert get_portal(level2, (5, 5)) == stairs2
