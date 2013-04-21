#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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
#   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

"""
Module for testing configuration DSL
"""
from pyherc.generators.level.prototiles import FLOOR_NATURAL

from mockito import mock
from hamcrest import assert_that, is_, equal_to, has_item #pylint: disable-msg=E0611
from pyherc.config.dsl import LevelConfiguration, Catacombs, natural_floor
from random import Random

class TestConfigDSL():
    """
    Tests for configuration DSL
    """
    def __init__(self):
        super(TestConfigDSL, self).__init__()

    def test_level_generator_factory_config_creation(self):
        """
        Test that LevelGeneratorFactoryConfig can be created
        """
        rooms = mock()
        partitioners = mock()
        decorators = mock()
        items = mock()
        creatures = mock()
        portals = mock()
        context = mock()

        config = (LevelConfiguration()
                    .with_rooms(rooms)
                    .with_partitioners(partitioners)
                    .with_decorators(decorators)
                    .with_items(items)
                    .with_creatures(creatures)
                    .with_portals(portals)
                    .with_contexts([context])
                    .build())

        assert_that(config.room_generators, is_(equal_to(rooms)))
        assert_that(config.level_partitioners, is_(equal_to(partitioners)))
        assert_that(config.decorators, is_(equal_to(decorators)))
        assert_that(config.item_adders, is_(equal_to(items)))
        assert_that(config.creature_adders, is_(equal_to(creatures)))
        assert_that(config.portal_adder_configurations, is_(equal_to(portals)))

    def test_catacombs_generator(self):
        """
        test that catacombs generator can be created
        """
        rng = Random()

        generator = (Catacombs()
                        .with_(natural_floor())
                        .located_at('upper catacombs')
                        .located_at('lower catacombs')
                        .with_(rng)
                        .build())

        assert_that(generator.floor_tile, is_(equal_to(FLOOR_NATURAL)))
        assert_that(generator.level_types, has_item('upper catacombs'))
        assert_that(generator.level_types, has_item('lower catacombs'))
        assert_that(generator.rng, is_(equal_to(rng)))
