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
Tests for SquareRoomGenerator room generator
'''
#pylint: disable=W0614
from pyherc.data import Level
from pyherc.generators.level.partitioners.section import Section
from pyherc.generators.level.room import SquareRoomGenerator
from hamcrest import * #pylint: disable=W0401
from pyherc.data.tiles import FLOOR_ROCK
from pyherc.data.tiles import WALL_GROUND
from pyherc.data.tiles import WALL_EMPTY

class TestSquareRoom():
    '''
    Tests for SquareRoomGenerator room generator
    '''
    def __init__(self):
        '''
        Default constructor
        '''
        self.level = None
        self.section = None
        self.generator = None

    def setup(self):
        """
        Setup the test case
        """
        self.level = Level((20, 20), FLOOR_ROCK, WALL_GROUND)
        self.section = Section((5, 5), (15, 15), self.level)
        self.generator = SquareRoomGenerator(FLOOR_ROCK, WALL_EMPTY)

    def test_generate_simple_room(self):
        '''
        Test that generator can create a simple room
        '''
        self.generator.generate_room(self.section)

        room_found = False
        for y_loc in range(20):
            for x_loc in range(20):
                if self.level.get_tile(x_loc, y_loc) != WALL_GROUND:
                    room_found = True

        print self.level.dump_string()

        assert_that(room_found, is_(True))

    def test_room_connections_are_placed(self):
        """
        Test that generating a square room will place 4 connectors
        """
        self.generator.generate_room(self.section)

        assert_that(self.section.room_connections, has_length(4))
