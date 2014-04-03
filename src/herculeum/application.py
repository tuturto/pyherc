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
Module for application level objects
"""
import logging
import sys

import herculeum.config.levels
import hy
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
        self.silent = False

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

    surface_manager = property(__get_surface_manager)
    action_factory = property(__get_action_factory)
    creature_generator = property(__get_creature_generator)
    player_generator = property(__get_player_generator)
    item_generator = property(__get_item_generator)
    level_generator_factory = property(__get_level_generator_factory)
    rng = property(__get_rng)
    rules_engine = property(__get_rules_engine)
