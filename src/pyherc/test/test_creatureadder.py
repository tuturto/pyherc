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
Tests for CreatureAdder
"""
#pylint: disable=W0614
from pyDoubles.framework import empty_stub #pylint: disable=F0401, E0611
from pyDoubles.framework import assert_that_method #pylint: disable=F0401, E0611
from hamcrest import * #pylint: disable=W0401

from pyherc.data import Level
from pyherc.data.tiles import FLOOR_ROCK
from pyherc.data.tiles import WALL_EMPTY
from pyherc.generators.creature import CreatureGenerator
import random

class TestCreatureAdder():
    """
    Tests for CreatureAdder
    """
    def __init__(self):
        """
        Default constructor
        """
        pass

    def setup(self):
        """
        Setup the test case
        """
        pass

    def test_adding_creatures(self):
        """
        Test basic case of adding creatures on the level
        """
        level = Level((60, 40), FLOOR_ROCK, WALL_EMPTY)

        level.set_location_type((10, 10), 'room')

        action_factory = empty_stub()
        creature_generator = CreatureGenerator(action_factory)

        configuration = CreatureAdderConfiguration()
        configuration.add_creature(min = 3, max = 4, name = 'rat')
        configuration.add_creature(min = 1, max = 1,
                                   name = 'dragon', location = 'room')
        creature_adder = CreatureAdder(creature_generator, configuration)

        creature_adder.add_creatures(level)

        assert_that(level.creatures, has_length(greater_than(3)))
        assert_that(level.creatures, has_length(less_than(6)))

        assert_that(level.creatures, has_creature('rat'))
        assert_that(level.creatures, has_creature('dragon'))
