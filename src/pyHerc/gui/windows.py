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
import logging
from pygame.locals import *

class MainWindow:

    def __init__(self):
        self.logger = logging.getLogger('pyHerc.gui.windows.MainWindow')

    def __init__(self,  application):
        """
        Initialises the main window
        Params:
            application: instance of currently running application
        """
        self.logger = logging.getLogger('pyHerc.gui.windows.MainWindow')
        self.logger.debug('Initialising MainWindow')
        pygame.init()
        self.width = application.config['resolution'][0]
        self.height = application.config['resolution'][1]
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(application.config['caption'])
        self.logger.debug('Initialising MainWindow done')

    def MainLoop(self):
        """
        This is the event handler for main window
        """
        self.logger.info('Main loop starting')
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.logger.info('Quit received, exiting')
                    sys.exit()
