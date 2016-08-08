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
Module for testing dungeon
"""

from mockito import mock
from pyherc.data import Portal, floor_tile, wall_tile, add_portal
from pyherc.data import get_portal
from pyherc.test.builders import LevelBuilder


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
        level = (LevelBuilder()
                 .with_size((20, 20))
                 .with_floor_tile(self.floor_rock)
                 .with_wall_tile(self.wall_empty)
                 .build())

        assert not (level is None)
        assert(floor_tile(level, (5, 5)) == self.floor_rock)
        assert(wall_tile(level, (0, 0)) == self.wall_empty)

    def test_stair_linking(self):
        """
        Test that stairs can be linked
        """
        level1 = (LevelBuilder()
                  .with_size((20, 20))
                  .with_floor_tile(self.floor_rock)
                  .with_wall_tile(self.wall_empty)
                  .build())

        level2 = (LevelBuilder()
                  .with_size((20, 20))
                  .with_floor_tile(self.floor_rock)
                  .with_wall_tile(self.wall_empty)
                  .build())

        stairs1 = Portal((None, None), None)

        stairs1.icon = 'stairs'
        add_portal(level1, (10, 10), stairs1)

        stairs2 = Portal((None, None), None)
        add_portal(level2, (5, 5), stairs2, stairs1)

        assert(stairs1.level == level1)
        assert(stairs1.location == (10, 10))
        assert(stairs1.get_other_end() == stairs2)

        assert(stairs2.level == level2)
        assert(stairs2.location == (5, 5))
        assert(stairs2.get_other_end() == stairs1)

        assert get_portal(level1, (10, 10)) == stairs1
        assert get_portal(level2, (5, 5)) == stairs2
