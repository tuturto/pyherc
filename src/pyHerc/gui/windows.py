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
import surfaceManager
import images
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
        self.logger.info('Initialising MainWindow')
        self.display = None
        self.application = application
        pygame.init()
        self.width = application.config['resolution'][0]
        self.height = application.config['resolution'][1]
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(application.config['caption'])
        surfaceManager.loadResources()

    def mainLoop(self):
        """
        This is the event handler for main window
        """
        self.logger.debug('Main loop starting')
        self.display = StartMenu(self.application, self.screen)
        self.display.mainLoop()

        self.logger.info('Quit received, exiting')
        sys.exit()

class StartMenu:
    """
    Start menu
    """

    def __init__(self,  application, screen):
        """
        Initialises start menu
        Params:
            application: instance of currently running application
        """
        self.running = 1
        self.selection = 0
        self.application = application
        self.screen = screen
        self.logger = logging.getLogger('pyHerc.gui.windows.StartMenu')
        self.logger.debug('initialising start menu')

        self.background = surfaceManager.getImage(images.image_start_menu)
        self.arrow = surfaceManager.getImage(images.image_start_menu_arrow)

        self.arrow_location = [(275 - self.arrow.get_width(), 204 - self.arrow.get_height() / 2),
                                        (275 - self.arrow.get_width(), 310 - self.arrow.get_height() / 2),
                                        (275 - self.arrow.get_width(), 417 - self.arrow.get_height() / 2)]

        self.arrow_rects = [Rect(self.arrow_location[0], self.arrow.get_size()),
                                            Rect(self.arrow_location[1], self.arrow.get_size()),
                                            Rect(self.arrow_location[2], self.arrow.get_size())]

        #TODO: use configuration
        self.dirty_rectangles = [Rect(0, 0, 800, 600)]

        self.logger.debug('start menu initialised')

    def mainLoop(self):
        """
        This is the event handler for start menu
        """
        self.logger.debug('Main loop starting')
        while self.running:

            self.updateDisplay()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.logger.info('Quit received, exiting')
                    self.running = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.dirty_rectangles.append(self.arrow_rects[self.selection])
                        self.selection = self.selection + 1
                        if self.selection > 2:
                            self.selection = 0
                        self.dirty_rectangles.append(self.arrow_rects[self.selection])
                    elif event.key == pygame.K_UP:
                        self.dirty_rectangles.append(self.arrow_rects[self.selection])
                        self.selection = self.selection - 1
                        if self.selection < 0:
                            self.selection = 2
                        self.dirty_rectangles.append(self.arrow_rects[self.selection])
                    elif event.key == pygame.K_SPACE:
                        if self.selection == 0:
                            self.logger.debug('new game selected')
                            #TODO: implement
                        elif self.selection == 1:
                            self.logger.debug('load game selected')
                            #TODO: implement
                        elif self.selection == 2:
                            self.logger.debug('exit selected')
                            self.running = 0

    def updateDisplay(self):
        """
        Draws this window on screen
        """
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.arrow, self.arrow_location[self.selection])

        pygame.display.update(self.dirty_rectangles)
        self.dirty_rectangles = []
