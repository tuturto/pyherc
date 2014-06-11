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
Module for testing main configuration
"""

#pylint: disable=W0614
import herculeum.config.levels
from hamcrest import assert_that, is_, not_none  # pylint: disable-msg=E0611
from herculeum.config import Configuration
from mockito import mock
from pyherc.data import Model
from pyherc.rules.inventory.interface import InventoryParameters


class TestMainConfiguration():
    """
    Tests for main configuration
    """
    def __init__(self):
        """
        Default constructor
        """
        self.config = None

    def setup(self):
        """
        Setup test case
        """
        self.config = Configuration(Model(),
                                    herculeum.config.levels,
                                    mock(),
                                    mock())

        self.config.initialise()

    def test_initialisation(self):
        """
        Test that main configuration can be read and initialised properly

        Note:
            This test reads configuration from resources directory
        """
        config = self.config
        assert_that(config.surface_manager, is_(not_none()))
        assert_that(config.action_factory, is_(not_none()))
        assert_that(config.item_generator, is_(not_none()))
        assert_that(config.creature_generator, is_(not_none()))
        assert_that(config.level_generator_factory, is_(not_none()))
        assert_that(config.level_size, is_(not_none()))
        assert_that(config.model, is_(not_none()))
        assert_that(config.rng, is_(not_none()))

    def test_upper_catacombs_generator(self):
        """
        Test that upper catacombs level generator can be retrieved
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('upper catacombs')

    def test_upper_crypt_generator(self):
        """
        Test that upper crypt level generator can be retrieved
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('upper crypt')

    def test_inventory_factory_has_been_initialised(self):
        """
        Test that inventory action factory has been initialised
        """
        factory = self.config.action_factory.get_sub_factory(
                            InventoryParameters(character = None,
                                                item = None,
                                                sub_action = 'pick up'))

        assert_that(factory, is_(not_none()))

    def test_player_character_generator_has_been_initialised(self):
        """
        Test that player character generator is initialised during
        configuration phase
        """
        assert_that(self.config.player_generator, is_(not_none()))
