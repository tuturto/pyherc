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
Tests for Connection
"""
import random

from hamcrest import assert_that, equal_to, is_
from pyherc.test.builders import LevelBuilder
from pyherc.generators.level.partitioners import Connection, new_section


class TestConnection():
    """
    Tests for connection
    """

    def test_translating_to_section(self):
        """
        Test that Connection can be translated to section coordinates
        """
        level = LevelBuilder().build()
        section = new_section((10, 10),
                              (20, 20),
                              level,
                              random.Random())

        connection = Connection(connection=None,
                                location=(20, 20),
                                direction="right",
                                section=section)

        translated_connection = connection.translate_to_section()

        assert_that(translated_connection.location, is_(equal_to((10, 10))))
