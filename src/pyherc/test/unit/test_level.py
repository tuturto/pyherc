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

from hamcrest import (assert_that, is_, equal_to,
                      contains_inanyorder)
from pyherc.data import Model, level_size, get_locations_by_tag
from pyherc.data import add_location_tag, add_location_feature, location_features
from pyherc.data.features import new_grave, feature_type
from pyherc.test.builders import LevelBuilder

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
        self.level = (LevelBuilder()
                      .with_size((20, 10))
                      .build())

    def test_get_size(self):
        """
        Test that Level can report size
        """
        assert_that(level_size(self.level), is_(equal_to((0, 19, 0, 9))))

    def test_manipulating_features(self):
        """
        Teset that features can be manipulated
        """
        add_location_feature(self.level, (5, 5),
                             new_grave(self.level, (5, 5), ['coin'], ['skeleton']))
        feature = list(location_features(self.level, (5, 5)))[0]

        assert_that(feature_type(feature), is_(equal_to('\ufdd0:cache')))


    def test_get_rooms(self):
        """
        Test that level can report what areas of it are marked as being room
        """
        add_location_tag(self.level, (5, 5), 'room')
        add_location_tag(self.level, (5, 6), 'room')
        add_location_tag(self.level, (8, 8), 'room')
        add_location_tag(self.level, (9, 8), 'room')

        rooms = get_locations_by_tag(self.level, 'room')

        assert_that(rooms, contains_inanyorder((5, 5), (5, 6),
                                               (8, 8), (9, 8)))

    def test_get_locations_by_type_does_not_report_all_locations(self):
        """
        Test that getting locations by type does not return all locations
        """
        add_location_tag(self.level, (5, 5), 'room')
        add_location_tag(self.level, (5, 6), 'room')
        add_location_tag(self.level, (8, 8), 'room')
        add_location_tag(self.level, (9, 8), 'room')

        add_location_tag(self.level, (6, 5), 'corridor')
        add_location_tag(self.level, (6, 6), 'corridor')
        add_location_tag(self.level, (6, 7), 'corridor')
        add_location_tag(self.level, (6, 8), 'corridor')

        rooms = get_locations_by_tag(self.level, 'room')

        assert_that(rooms, contains_inanyorder((5, 5), (5, 6),
                                               (8, 8), (9, 8)))
