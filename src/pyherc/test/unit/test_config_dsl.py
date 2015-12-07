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
Module for testing configuration DSL
"""
from random import Random

from hamcrest import assert_that, equal_to, has_item, is_
from mockito import mock
from pyherc.config.dsl import Catacombs, LevelConfiguration, natural_floor
from pyherc.generators.level.prototiles import FLOOR_NATURAL


class TestConfigDSL():
    """
    Tests for configuration DSL
    """
    def __init__(self):
        super().__init__()

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
