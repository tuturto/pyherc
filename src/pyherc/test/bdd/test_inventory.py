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
Module for inventory management tests
"""
from hamcrest import assert_that
from pyherc.test.cutesy import (carrying, Dagger, drop, Goblin, has_dropped,
                                Level, make, middle_of, place)


class TestDroppingItems():
    """
    Tests for dropping items
    """
    def __init__(self):
        """
        Default constructor
        """
        super().__init__()

    def test_dropping_item(self):
        """
        Items dropped by character should end on the floor
        """
        dagger = Dagger()
        Uglak = Goblin(carrying(dagger))
        place(Uglak, middle_of(Level()))

        make(Uglak, drop(dagger))

        assert_that(Uglak, has_dropped(dagger))
