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

    def test_first_gate_generator(self):
        """
        Test that first gate level generator can be retrieved and used
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('first gate')
        level = generator(None)

    def test_upper_mines_generator(self):
        """
        Test that upper mines level generator can be retrieved
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('upper mines')
        level = generator(None)

    def test_lower_mines_generator(self):
        """
        Test that lower mines level can be created
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('lower mines')
        level = generator(None)        

    def test_forge_generator(self):
        """
        Test that forge can be generated
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('forge')
        level = generator(None)

    def test_lower_caverns_generator(self):
        """
        Test that lower caverns can be generated
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('lower caverns')
        level = generator(None)

    def test_middle_caverns_generator(self):
        """
        Test that middle caverns can be generated
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('middle caverns')
        level = generator(None)

    def test_upper_caverns_generator(self):
        """
        Test that upper caverns can be generated
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('upper caverns')
        level = generator(None)

    def test_second_gate_generator(self):
        """
        Test that second gate can be generated
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('second gate')
        level = generator(None)

    def test_lower_maze_generator(self):
        """
        Test that lower maze can be generated
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('lower maze')
        level = generator(None)

    def test_courtyard_generator(self):
        """
        Test that courtyard can be generated
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('courtyard')
        level = generator(None)

    def test_upper_maze_generator(self):
        """
        Test that upper maze can be generated
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('upper maze')
        level = generator(None)

    def test_third_gate_generator(self):
        """
        Test that third gate can be generated
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('third gate')
        level = generator(None)

    def test_lower_catacombs_generator(self):
        """
        Test that lower catacombs can be generated
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('lower catacombs')
        level = generator(None)

    def test_central_catacombs_generator(self):
        """
        Test that central catacombs can be generated
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('central catacombs')
        level = generator(None)

    def test_upper_catacombs_generator(self):
        """
        Test that upper catacombs can be generated
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('upper catacombs')
        level = generator(None)

    def test_final_gate_generator(self):
        """
        Test that final gate can be generated
        """
        factory = self.config.level_generator_factory
        generator = factory.get_generator('final gate')
        level = generator(None)

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
