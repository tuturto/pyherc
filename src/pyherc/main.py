#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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
Main entry point for pyherc - game
"""
import os.path
import sys, getopt
import logging

INSTALL_PATH = os.path.abspath(".")
sys.path.append(INSTALL_PATH)

import pygame
import pgu.gui
from pyherc.gui.windows import MainWindow
from pyherc.gui.startmenu import StartMenu
from pyherc.config import Configuration
from pyherc.data.model import Model

if not pygame.font:
    print 'Warning, fonts disabled'

if not pygame.mixer:
    print 'Warning, sound disabled'

print '#   pyherc is free software: you can redistribute it and/or modify'
print '#   it under the terms of the GNU General Public License as published by'
print '#   the Free Software Foundation, either version 3 of the License, or'
print '#   (at your option) any later version.'
print '#'
print '#   pyherc is distributed in the hope that it will be useful,'
print '#   but WITHOUT ANY WARRANTY; without even the implied warranty of'
print '#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the'
print '#   GNU General Public License for more details.'
print '#'
print '#   You should have received a copy of the GNU General Public License'
print '#   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.'

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

    def process_command_line(self, argv):
        """
        Process command line options
        """
        try:
            opts, args = getopt.getopt(argv, 'l:x', ['logging='])
        except getopt.GetoptError:
            print('')
            print('Failed to process parameters')
            self.usage()
            sys.exit()

        for opt, arg in opts:
            if opt in ('-l', '--logging'):
                if arg.lower() == 'debug':
                    self.log_level = logging.DEBUG
                elif arg.lower() == 'info':
                    self.log_level = logging.INFO
                elif arg.lower() == 'warning':
                    self.log_level = logging.WARNING
                elif arg.lower() == 'error':
                    self.log_level = logging.ERROR
                elif arg.lower() == 'critical':
                    self.log_level = logging.CRITICAL
                else:
                    print('')
                    print('Unknown logging level: ' + arg)
                    self.usage()
                    sys.exit(0)

        if self.log_level == None:
            self.log_level = logging.ERROR

    def usage(self):
        """
        Shows usage info
        """
        print('')
        print('Usage:')
        print('  -l --logging=')
        print('    debug, info, warning, error, critical')
        print('')

    def load_configuration(self):
        """
        Load configuration
        """
        self.world = Model()
        self.config = Configuration(self.base_path, self.world)
        self.config.initialise()

    def run(self):
        """
        Starts the application
        """
        self.screen = pygame.display.set_mode((800, 600),
                                              pygame.SWSURFACE)
        self.gui = MainWindow(self,
                              self.base_path,
                              self.surface_manager,
                              self.screen)
        menu = StartMenu(self,
                         self.screen,
                         self.surface_manager)
        self.gui.connect(pgu.gui.QUIT, self.gui.quit, None)
        self.gui.run(menu, screen = self.screen)

    def __get_surface_manager(self):
        """
        Get surface manager
        """
        return self.config.surface_manager

    def start_logging(self):
        '''
        Start logging for the system
        '''
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
        self.gui.change_state(state)

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

    def detect_resource_directory(self):
        '''
        Detects location of resources directory and updates self.base_path
        '''
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

if __name__ == "__main__":
    APP = Application()
    APP.detect_resource_directory()
    APP.process_command_line(sys.argv[1:])
    APP.start_logging()
    APP.load_configuration()
    APP.run()
