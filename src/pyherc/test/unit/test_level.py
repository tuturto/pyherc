#!/usr/bin/env python3
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
Tests for Level
"""

#pylint: disable=W0614
from hamcrest import (assert_that,  # pylint: disable-msg=E0611
                      contains_inanyorder)
from pyherc.data import Level


class TestLevel:
    """
    Tests for Level
    """
    def __init__(self):
        """
        Default constructor
        """
        self.level = None

    def setup(self):
        """
        Setup test case
        """
        self.level = Level(size = (20, 10))

    def test_get_size(self):
        """
        Test that Level can report size
        """
        size = self.level.get_size()

        assert size == (21, 11)

    def test_get_rooms(self):
        """
        Test that level can report what areas of it are marked as being room
        """
        self.level.set_location_type((5, 5), 'room')
        self.level.set_location_type((5, 6), 'room')
        self.level.set_location_type((8, 8), 'room')
        self.level.set_location_type((9, 8), 'room')

        rooms = self.level.get_locations_by_type('room')

        assert_that(rooms, contains_inanyorder((5, 5), (5, 6),
                                               (8, 8), (9, 8)))

    def test_get_locations_by_type_does_not_report_all_locations(self):
        """
        Test that getting locations by type does not return all locations
        """
        self.level.set_location_type((5, 5), 'room')
        self.level.set_location_type((5, 6), 'room')
        self.level.set_location_type((8, 8), 'room')
        self.level.set_location_type((9, 8), 'room')

        self.level.set_location_type((6, 5), 'corridor')
        self.level.set_location_type((6, 6), 'corridor')
        self.level.set_location_type((6, 7), 'corridor')
        self.level.set_location_type((6, 8), 'corridor')

        rooms = self.level.get_locations_by_type('room')

        assert_that(rooms, contains_inanyorder((5, 5), (5, 6),
                                               (8, 8), (9, 8)))
