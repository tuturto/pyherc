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
Tests for SquareRoom room generator
'''

from pyherc.data import Level
from pyherc.generators.level.partitioners.section import Section
from pyherc.generators.level.room import SquareRoom
from mock import Mock
from pyherc.data.tiles import FLOOR_ROCK
from pyherc.data.tiles import WALL_GROUND
from pyherc.data.tiles import WALL_EMPTY

class TestSquareRoom():
    '''
    Tests for SquareRoom room generator
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        pass

    def test_generate_simple_room(self):
        '''
        Test that generator can create a simple room
        '''
        level = Level((20, 20), FLOOR_ROCK, WALL_GROUND)

        mock_corners = Mock(return_value = [
                                                 (5, 5),
                                                 (15, 15)])

        class MockSection(Section):
            """Simple mock for section object"""
            def __init__(self):
                """Default constructor"""
                pass
            @property
            def corners(self):
                """Override corners in order to mock them"""
                return mock_corners()
            @property
            def width(self):
                """Override width to work with mocking"""
                return 10
            @property
            def height(self):
                """Override height to work with mocking"""
                return 10
            @property
            def left_edge(self):
                """Override left_edge to work with mocking"""
                return 5
            @property
            def top_edge(self):
                """Override top_edge to work with mocking"""
                return 5

        mock_section = MockSection()

        generator = SquareRoom(FLOOR_ROCK, WALL_EMPTY)
        generator.generate_room(level, mock_section)

        room_found = False
        for y_loc in range(20):
            for x_loc in range(20):
                if level.get_tile(x_loc, y_loc) != WALL_GROUND:
                    room_found = True

        assert room_found
