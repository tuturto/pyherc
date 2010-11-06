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

import os, sys
import pygame
import gui
import logging

from pygame.locals import *
from gui.windows import MainWindow
from data.model import Model

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

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
        self.loadConfiguration()
        self.config = None
        self.gui = None
        self.world = None

    def loadConfiguration(self):
        """
        Load configuration

        For now this is just a simple object initialisation
        """
        self.config = {}
        self.config['resolution'] = (800, 600)
        self.config['caption'] = 'Herculeum'
        self.config['logging'] = {}
        self.config['logging']['level'] = logging.DEBUG

    def run(self):
        """
        Starts the application
        """
        self.gui = MainWindow(self)
        self.world = Model()
        self.gui.MainLoop()


    def startLogging(self):
        logging.basicConfig(level=self.config['logging']['level'])
        logger = logging.getLogger('pyHerc.main.Application')
        logger.info("Logging started")

if __name__ == "__main__":
    app = Application()
    app.loadConfiguration()
    app.startLogging()
    app.run()
