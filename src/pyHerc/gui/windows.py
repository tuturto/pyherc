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
import rules.character
import rules.moving
import data.model
import data.tiles
import generators.dungeon
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
            screen: display to draw onto
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
        while self.running and self.application.running:

            self.__updateDisplay()

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
                            self.__startNewGame()
                            self.dirty_rectangles = [Rect(0, 0, 800, 600)]
                        elif self.selection == 1:
                            self.logger.debug('load game selected')
                            #TODO: implement
                        elif self.selection == 2:
                            self.logger.debug('exit selected')
                            self.running = 0

        self.logger.debug('main loop finished')

    def __startNewGame(self):
        newWindow = StartNewGameWindow(self.application, self.screen)
        newWindow.mainLoop()
        self.application.world.player = newWindow.character
        newWindow = GameWindow(self.application, self.screen)
        newWindow.mainLoop()

    def __updateDisplay(self):
        """
        Draws this window on screen
        """
        if len(self.dirty_rectangles) > 0:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.arrow, self.arrow_location[self.selection])

            pygame.display.update(self.dirty_rectangles)
            self.dirty_rectangles = []

class StartNewGameWindow:
    """
    Window that is displayed when player starts a new game
    """
    def __init__(self,  application, screen):
        self.running = 1
        self.application = application
        self.screen = screen
        self.logger = logging.getLogger('pyHerc.gui.windows.StartNewGameWindow')
        self.logger.debug('initialising display')
        self.logger.debug('display initialised')
        self.character = None

    def mainLoop(self):
        self.logger.debug('main loop starting')
        #TODO: implement menu here
        self.__generateNewGame()
        self.logger.debug('main loop finished')

    def __generateNewGame(self):
        #TODO: implement properly
        self.application.world = data.model.Model()
        generator = generators.dungeon.DungeonGenerator()
        generator.generateDungeon(self.application.world)
        self.character = rules.character.createCharacter('human', 'fighter')
        self.character.level = self.application.world.dungeon.levels
        self.character.location = (1, 1)
        self.character.name = 'Adventurer'

    def __updateDisplay(self):
        """
        Draws this window on screen
        """

class GameWindow:
    """
    Window that displays the playing world
    """
    def __init__(self,  application, screen):
        self.logger = logging.getLogger('pyHerc.gui.windows.GameWindow')
        self.logger.debug('initialising display')
        self.running = 1
        self.application = application
        self.screen = screen
        self.fullUpdate = 1
        self.background = surfaceManager.getImage(images.image_play_area)
        self.logger.debug('display initialised')

    def mainLoop(self):
        self.logger.debug('main loop starting')
        while self.running and self.application.running:
            #TODO: implement
            for event in pygame.event.get():
                model = self.application.world
                player = model.player

                if event.type == pygame.QUIT:
                    self.logger.info('Quit received, exiting')
                    self.application.running = 0
                    self.running = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == K_q:
                        self.running = 0
                    if event.key == K_KP8:
                        rules.moving.move(model, player, 1)
                    elif event.key == K_KP9:
                        rules.moving.move(model, player, 2)
                    elif event.key == K_KP6:
                        rules.moving.move(model, player, 3)
                    elif event.key == K_KP3:
                        rules.moving.move(model, player, 4)
                    elif event.key == K_KP2:
                        rules.moving.move(model, player, 5)
                    elif event.key == K_KP1:
                        rules.moving.move(model, player, 6)
                    elif event.key == K_KP4:
                        rules.moving.move(model, player, 7)
                    elif event.key == K_KP7:
                        rules.moving.move(model, player, 8)
            self.__updateDisplay()
        self.logger.debug('main loop finished')

    def __updateDisplay(self):
        """
        Draws this window on screen
        """
        if self.fullUpdate == 1:
            player = self.application.world.player
            level = player.level

            self.screen.blit(self.background, (0, 0))
            #TODO: make more generic
            sy = 0
            for y in range(player.location[1] - 7, player.location[1] + 8):
                sx = 0
                for x in range(player.location[0] - 12, player.location[0] + 13):
                    #draw floor and walls
                    if x >= 0 and y >= 0 and x <= len(level.floor)-1 and y <= len(level.floor[x])-1:
                        tile = surfaceManager.getIcon(level.floor[x][y])
                        self.screen.blit(tile, (sx * 32, sy *32))
                        if not level.walls[x][y] == data.tiles.wall_empty:
                            tile = surfaceManager.getIcon(level.walls[x][y])
                            self.screen.blit(tile, (sx * 32, sy *32))
                    else:
                        #draw empty
                        tile = surfaceManager.getIcon(data.tiles.floor_empty)
                        self.screen.blit(tile, (sx * 32, sy *32))
                    sx = sx + 1
                sy = sy + 1
                sx = 0

            #draw items
            for item in level.items:
                x = item.location[0] - player.location[0] + 13
                y = item.location[1] - player.location[1] + 8
                if x >= 0 and y >= 0 and x <= 24 and y <= 14:
                    tile = surfaceManager.getIcon(item.icon)
                    self.screen.blit(tile, (x * 32, y *32))

            tile = surfaceManager.getIcon(player.icon)
            self.screen.blit(tile, (384, 224))
            pygame.display.update()

