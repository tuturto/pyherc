#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
#
#   This file is part of pyHerc.
#
#   pyHerc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyHerc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyHerc.  If not, see <http://www.gnu.org/licenses/>.

import sys, getopt
import pygame
import logging

from pyHerc.gui.windows import MainWindow

if not pygame.font:
    print 'Warning, fonts disabled'

if not pygame.mixer:
    print 'Warning, sound disabled'

print '#   pyHerc is free software: you can redistribute it and/or modify'
print '#   it under the terms of the GNU General Public License as published by'
print '#   the Free Software Foundation, either version 3 of the License, or'
print '#   (at your option) any later version.'
print '#'
print '#   pyHerc is distributed in the hope that it will be useful,'
print '#   but WITHOUT ANY WARRANTY; without even the implied warranty of'
print '#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the'
print '#   GNU General Public License for more details.'
print '#'
print '#   You should have received a copy of the GNU General Public License'
print '#   along with pyHerc.  If not, see <http://www.gnu.org/licenses/>.'

class Application:
    """
    This class represents main application
    """

    def __init__(self):
        self.config = None
        self.gui = None
        self.world = None
        self.running = 1

    def load_configuration(self, argv):
        """
        Load configuration and process command line options
        @param argv: command line arguments
        """
        self.config = {}
        self.config['logging'] = {}
        self.config['explore'] = 0

        try:
            opts, args = getopt.getopt(argv, 'l:x', ['logging=',
                                                                    'explore'])
        except getopt.GetoptError:
            print('')
            print('Failed to process parameters')
            self.usage()
            sys.exit()

        for opt, arg in opts:
            if opt in ('-l', '--logging'):
                if arg.lower() == 'debug':
                    self.config['logging']['level'] = logging.DEBUG
                elif arg.lower() == 'info':
                    self.config['logging']['level'] = logging.INFO
                elif arg.lower() == 'warning':
                    self.config['logging']['level'] = logging.WARNING
                elif arg.lower() == 'error':
                    self.config['logging']['level'] = logging.ERROR
                elif arg.lower() == 'critical':
                    self.config['logging']['level'] = logging.CRITICAL
                else:
                    print('')
                    print('Unknown logging level: ' + arg)
                    self.usage()
                    sys.exit(0)
            if opt in ('-x', '--explore'):
                self.config['explore'] = 1

        self.config['resolution'] = (800, 600)
        self.config['caption'] = 'Herculeum'
        if not 'level' in self.config['logging'].keys():
            self.config['logging']['level'] = logging.ERROR

    def usage(self):
        """
        Shows usage info
        """
        print('')
        print('Usage:')
        print('  -l --logging=')
        print('    debug, info, warning, error, critical')
        print('')

    def run(self):
        """
        Starts the application
        """
        self.gui = MainWindow(self)
        self.gui.mainLoop()

    def start_logging(self):
        '''
        Start logging for the system
        '''
        logging.basicConfig(level=self.config['logging']['level'])
        logger = logging.getLogger('pyHerc.main.Application')
        logger.info("Logging started")

if __name__ == "__main__":
    application = Application()
    application.load_configuration(sys.argv[1:])
    application.start_logging()
    application.run()
