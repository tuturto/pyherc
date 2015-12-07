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
Tests for Level
"""

from hamcrest import (assert_that, is_, equal_to,
                      contains_inanyorder)
from pyherc.data import (Model, level_size, get_locations_by_tag,
                         add_location_tag, add_location_feature,
                         location_features)
from pyherc.data.features import new_cache, feature_type
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
                             new_cache(self.level, (5, 5), ['coin'],
                                       ['skeleton']))
        feature = list(location_features(self.level, (5, 5)))[0]

        assert_that(feature_type(feature), is_(equal_to('cache')))


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
