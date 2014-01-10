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
Module for inventory management tests
"""
from pyherc.test.cutesy import Dagger, Goblin, carrying
from pyherc.test.cutesy import place, middle_of, Level
from pyherc.test.cutesy import make, drop
from pyherc.test.cutesy import has_dropped
from hamcrest import assert_that #pylint: disable-msg=E0611

#pylint: disable=C0103
class TestDroppingItems():
    """
    Tests for dropping items
    """
    def __init__(self):
        """
        Default constructor
        """
        super(TestDroppingItems, self).__init__()

    def test_dropping_item(self):
        """
        Items dropped by character should end on the floor
        """
        dagger = Dagger()
        Uglak = Goblin(carrying(dagger))
        place(Uglak, middle_of(Level()))

        make(Uglak, drop(dagger))

        assert_that(Uglak, has_dropped(dagger))
