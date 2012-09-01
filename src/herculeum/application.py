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
Module for application level objects
"""
import os.path
from herculeum.config import Configuration
from pyherc.data.model import Model
import sys
import logging
import herculeum.config.levels

from herculeum.gui import MainWindow
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QFile, QLatin1String

class Application(object):
    """
    This class represents main application
    """

    def __init__(self):
        super(Application, self).__init__()
        self.config = None
        self.gui = None
        self.world = None
        self.running = 1
        self.base_path = None
        self.logger = None
        self.screen = None
        self.log_level = None

        self.qt_app = QApplication(sys.argv)

    def process_command_line(self):
        """
        Process command line options
        """
        log_levels = {'debug': logging.DEBUG,
                      'info': logging.INFO,
                      'warning': logging.WARNING,
                      'error': logging.ERROR,
                      'critical': logging.CRITICAL}
        args = sys.argv
        for argument in args:
            if argument in log_levels:
                self.log_level = log_levels[argument]

    def load_configuration(self):
        """
        Load configuration
        """
        file = QFile(os.path.join(self.base_path, 'herculeum.qss'));
        file.open(QFile.ReadOnly)
        styleSheet = QLatin1String(file.readAll());
        self.qt_app.setStyleSheet(styleSheet);

        self.world = Model()
        self.config = Configuration(self.base_path, self.world)
        self.config.initialise(herculeum.config.levels)

    def run(self):
        """
        Starts the application
        """
        main_window = MainWindow(APP,
                                 APP.surface_manager)
        sys.exit(self.qt_app.exec_())

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

    def change_state(self, state):
        """
        Change state of the gui

        Args:
            state: String specifying which state to display
        """
        #TODO: change state
        #self.gui.change_state(state)

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

    def detect_resource_directory(self):
        """
        Detects location of resources directory and updates self.base_path
        """
        search_directory = '.'
        current = os.path.normpath(os.path.join(os.getcwd(), search_directory))

        while not os.path.exists(os.path.join(current, 'resources')):
            search_directory = search_directory +'/..'
            current = os.path.normpath(os.path.join(os.getcwd(),
                                                    search_directory))

        self.base_path = os.path.join(current, 'resources')

    surface_manager = property(__get_surface_manager)
    action_factory = property(__get_action_factory)
    creature_generator = property(__get_creature_generator)
    item_generator = property(__get_item_generator)
    level_generator_factory = property(__get_level_generator_factory)
    rng = property(__get_rng)
    rules_engine = property(__get_rules_engine)

render = None
APP = Application()
