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
Module for application level objects
"""
import logging
import sys

import herculeum.config.levels
from herculeum.config import Configuration
from pyherc.aspects import set_logger
from pyherc.data.model import Model


class Application():
    """
    This class represents main application
    """

    def __init__(self):
        super().__init__()
        self.config = None
        self.gui = None
        self.world = None
        self.running = 1
        self.logger = None
        self.screen = None
        self.log_level = None

    def load_configuration(self, controls, surface_manager):
        """
        Load configuration
        """
        self.world = Model()
        self.config = Configuration(self.world,
                                    herculeum.config.levels,
                                    controls,
                                    surface_manager)

        self.config.initialise()

    def run(self, user_interface):
        """
        Starts the application
        """
        user_interface.show_main_window()

    def enable_cheat(self):
        """
        Enables cheat mode

        .. versionadded:: 0.9
        """
        print('Cheat code activated')
        for spec in self.level_generator_factory.portal_adder_configurations:
            spec.chance = 100

    def __get_surface_manager(self):
        """
        Get surface manager
        """
        return self.config.surface_manager

    def start_logging(self):
        """
        Start logging for the system
        """
        if self.log_level != 'none':
            logging.basicConfig(filename='pyherc.log',
                                level=self.log_level)
        self.logger = logging.getLogger('pyherc.main.Application')
        self.logger.info("Logging started")

    def __get_action_factory(self):
        """
        Get action factory instance

        Returns:
            ActionFactory
        """
        return self.config.action_factory

    def __get_creature_generator(self):
        """
        Get creature generator

        Returns:
            CreatureGenerator
        """
        return self.config.creature_generator

    def __get_item_generator(self):
        """
        Get item generator

        Returns:
            ItemGenerator
        """
        return self.config.item_generator

    def __get_level_generator_factory(self):
        """
        Get level generator factory
        """
        return self.config.level_generator_factory

    def __get_rng(self):
        """
        Get random number generator
        """
        return self.config.rng

    def __get_rules_engine(self):
        """
        Get rules engine
        """
        return self.config.rules_engine

    def __get_player_generator(self):
        """
        Get player generator
        """
        return self.config.player_generator

    def __get_trap_generator(self):
        """
        Get trap generator
        """
        return self.config.trap_generator

    surface_manager = property(__get_surface_manager)
    action_factory = property(__get_action_factory)
    creature_generator = property(__get_creature_generator)
    player_generator = property(__get_player_generator)
    trap_generator = property(__get_trap_generator)
    item_generator = property(__get_item_generator)
    level_generator_factory = property(__get_level_generator_factory)
    rng = property(__get_rng)
    rules_engine = property(__get_rules_engine)
