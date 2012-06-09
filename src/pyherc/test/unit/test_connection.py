#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
Tests for Connection
"""
#pylint: disable=W0614
from pyherc.generators.level.partitioners.section import Section, Connection
from pyherc.data import Level
from pyherc.data.tiles import FLOOR_EMPTY, FLOOR_ROCK, WALL_EMPTY, WALL_GROUND
from mockito import mock
from hamcrest import * #pylint: disable=W0401
import random

class TestConnection():
    """
    Tests for connection
    """

    def test_translating_to_section(self):
        """
        Test that Connection can be translated to section coordinates
        """
        level = mock(Level)
        section = Section(corner1 = (10, 10),
                          corner2 = (20, 20),
                          level = level,
                          random_generator = random.Random())

        connection = Connection(connection = None,
                             location = (20, 20),
                             direction = "right",
                             section = section)

        translated_connection = connection.translate_to_section()

        assert_that(translated_connection.location, is_(equal_to((10, 10))))
