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
Tests for Level
"""

#pylint: disable=W0614
from pyherc.data import Level
from hamcrest import * #pylint: disable=W0401

class TestLevel:
    """
    Tests for Level
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def test_get_size(self):
        """
        Test that Level can report size
        """
        level = Level(size = (20, 10))
        size = level.get_size()

        assert size == (21, 11)

    def test_get_rooms(self):
        """
        Test that level can report what areas of it are marked as being room
        """
        level = Level((20, 10))

        level.room[5][5] = True
        level.room[5][6] = True
        level.room[8][8] = True
        level.room[9][8] = True

        rooms = level.get_rooms()

        assert_that(rooms, contains_inanyorder((5, 5), (5, 6),
                                               (8, 8), (9, 8)))
