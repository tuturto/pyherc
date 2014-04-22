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
Tests for calendar
"""

import hy
from hamcrest import assert_that, has_item
from pyherc.data import SpecialTime
from pyherc.rules.calendar import get_special_events


class TestCalendar():
    """
    Tests for calendar
    """
    def __init__(self):
        super().__init__()

    def test_chrismas(self):
        """
        24th, 25th and 26th of December should be christmas
        """
        events = get_special_events(2013, 12, 24)

        assert_that(events, has_item(SpecialTime.christmas))
