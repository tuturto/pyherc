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
Module for various windows used in game
"""

import pygame
import logging
import images
import dialogs
import pyherc.rules.character
import pyherc.data.model
import pyherc.data.tiles
import pyherc.rules.items
import pyherc.rules.ending
import pyherc.rules.time
import pyherc.generators.dungeon
import pyherc.rules.tables
import pyherc.gui.startmenu
import pgu.gui.app
from pyherc.rules.public import MoveParameters
from pyherc.rules.public import AttackParameters
from pyherc.rules.los import get_fov_matrix
from pygame.locals import K_ESCAPE, K_PERIOD
from pygame.locals import K_d, K_w, K_r, K_q,  K_i
from pygame.locals import K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9


class MainWindow(pgu.gui.app.App):
    """
    Main window of the game
    """

    def __init__(self,  application, base_path, surface_manager, screen, theme=None, **params):
        """
        Initialises the main window
        @param application: instance of currently running application
        @param base_path: location of resources directory
        @surface_manager: optional SurfaceManger to use for loading resources
        """
        super(MainWindow, self).__init__(theme, **params)
        self.logger = logging.getLogger('pyherc.gui.windows.MainWindow')
        self.logger.info('Initialising MainWindow')
        self.display = None
        self.application = application
        pygame.init()
        self.width = application.config['resolution'][0]
        self.height = application.config['resolution'][1]
        self.screen = screen
        pygame.display.set_caption(application.config['caption'])

        self.surface_manager = surface_manager

class StartNewGameWindow:
    """
    Window that is displayed when player starts a new game
    """
    def __init__(self,  application, screen, surface_manager = None):
        self.running = 1
        self.application = application
        self.screen = screen
        self.logger = logging.getLogger('pyherc.gui.windows.StartNewGameWindow')
        self.logger.debug('initialising display')

        self.surface_manager = surface_manager
        if self.surface_manager == None:
            self.logger.warn('Surface manager not specified, defaulting to the system one.')
            self.surface_manager = pyherc.gui.surfaceManager.SurfaceManager()
            self.surface_manager.loadResources()

        self.logger.debug('display initialised')
        self.character = None

    def mainLoop(self):
        """
        Main loop of the window
        """
        self.logger.debug('main loop starting')
        #TODO: implement menu here
        self.__generateNewGame()
        self.logger.debug('main loop finished')

    def __generateNewGame(self):
        """
        Generate a new game
        """
        #TODO: implement properly
        self.application.world = pyherc.data.model.Model()

        self.application.initialise_factories(self.application.world)

        tables = pyherc.rules.tables.Tables()
        tables.load_tables(self.application.base_path)
        self.application.world.tables = tables
        #TODO: load tables for model
        if self.application.config['explore']:
            self.logger.warn('starting in explore mode')
            self.application.world.config['explore'] = 1
        else:
            self.application.world.config['explore'] = 0

        self.character = pyherc.rules.character.create_character('human', 'fighter', self.application.get_action_factory())
        self.application.world.player = self.character
        generator = pyherc.generators.dungeon.DungeonGenerator(self.application.get_action_factory())
        generator.generate_dungeon(self.application.world)
        self.character.level = self.application.world.dungeon.levels
        # self.character.location = (1, 1)
        self.character.name = 'Adventurer'

    def __updateDisplay(self):
        """
        Draws this window on screen
        """

class GameWindow:
    """
    Window that displays the playing world
    """
    def __init__(self,  application, screen, surface_manager = None):
        self.logger = logging.getLogger('pyherc.gui.windows.GameWindow')
        self.logger.debug('initialising display')
        self.application = application
        self.screen = screen
        self.fullUpdate = 1
        self.surface_manager = surface_manager
        if self.surface_manager == None:
            self.logger.warn('Surface manager not specified, defaulting to the system one.')
            self.surface_manager = pyherc.gui.surfaceManager.SurfaceManager()
            self.surface_manager.loadResources()

        if screen != None:
            self.background = self.surface_manager.getImage(images.image_play_area)
            self.console = self.surface_manager.getImage(images.image_console)
        self.logger.debug('display initialised')
        self.moveKeyMap = {K_KP8:1, K_KP9:2, K_KP6:3, K_KP3:4, K_KP2:5, K_KP1:6,
                                    K_KP4:7, K_KP7:8, K_KP5:9}
        self.eventHistory = []

    def __handlePlayerInput(self):
        """
        Handle player input
        """
        model = self.application.world
        player = model.player
        playerTick = player.tick

        for event in pygame.event.get():
            if playerTick == player.tick:
                if event.type == pygame.QUIT:
                    self.logger.info('Quit received, exiting')
                    self.application.running = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        #quit
                        self.application.world.end_condition = 1
                    elif event.key in self.moveKeyMap.keys():
                        player.level.full_update_needed = True
                        #handle moving
                        direction = self.moveKeyMap[event.key]
                        action = player.create_action(
                                        MoveParameters(player, direction, 'walk')
                                        )

                        if action.is_legal():
                            #check in case player escaped
                            if player.level != None:
                                action.execute()
                        else:
                            target = player.level.get_creature_at(action.new_location)
                            if target != None:
                                #TODO: melee / unarmed selection
                                player.execute_action(
                                        AttackParameters(player, target, 'unarmed')
                                        )
                    elif event.key == K_PERIOD:
                        #pick up items
                        items = player.level.get_items_at(player.location)
                        if len(items) > 1:
                            dialog = dialogs.Inventory(self.application, self.screen, self.surface_manager)
                            items = dialog.show(items)
                        for item in items:
                            pyherc.rules.items.pick_up(model, player, item)
                        player.level.full_update_needed = True
                    elif event.key == K_i:
                        #display inventory
                        dialog = dialogs.Inventory(self.application, self.screen, self.surface_manager)
                        dialog.show(player.inventory, 0)
                        player.level.full_update_needed = True
                    elif event.key == K_d:
                        #drop items
                        dialog = dialogs.Inventory(self.application, self.screen, self.surface_manager)
                        dropItems = dialog.show(player.inventory)
                        for item in dropItems:
                            pyherc.rules.items.drop(model, player, item)
                        player.level.full_update_needed = True
                    elif event.key == K_w:
                        #wield weapons
                        dialog = dialogs.Inventory(self.application, self.screen, self.surface_manager)
                        wieldItems = dialog.show(player.inventory, 2)
                        for item in wieldItems:
                            pyherc.rules.items.wield(model, player, item, True)
                        player.level.full_update_needed = True
                    elif event.key == K_r:
                        #unwield weapons
                        dialog = dialogs.Inventory(self.application, self.screen, self.surface_manager)
                        removable = dialog.show(player.weapons)
                        for item in removable:
                            pyherc.rules.items.unwield(model, player, item)
                        player.level.full_update_needed = True
                    elif event.key == K_q:
                        #quaff potion
                        dialog = dialogs.Inventory(self.application, self.screen, self.surface_manager)
                        potion = dialog.show(player.inventory, 1)
                        if len(potion) == 1:
                            pyherc.rules.items.drink_potion(model, player, potion[0])
                        player.level.full_update_needed = True
            else:
                return

    def mainLoop(self):
        """
        Main loop of the game
        """
        self.logger.debug('main loop starting')
        while self.application.world.end_condition == 0 and self.application.running:

            model = self.application.world

            creature = pyherc.rules.time.get_next_creature(model)

            #TODO: do not paint screen all the time
            if creature == model.player:
                if self.application.world.player.level != None:
                    self.__updateDisplay()
                self.__handlePlayerInput()
                self.getNewEvents()
                if self.application.world.player.level != None:
                    self.__updateDisplay()
            else:
                if self.application.world.player.level != None:
                    creature.act(self.application.world)
                    #TODO: set dirty rectangles properly
                    self.getNewEvents()
                    self.application.world.player.level.full_update_needed = True
                    #TODO: when dirty rectangles work, uncomment this
                    #self.__updateDisplay()

        self.logger.debug('main loop finished')

    def getNewEvents(self):
        """
        Process memory of player character and store interesting events
        """
        for event in self.application.world.player.short_term_memory:
            if event['type'] == 'melee':
                newLine = event['attacker'].name + ' attacks'
                if event['hit'] == 0:
                    newLine = newLine + ' but misses'
                else:
                    newLine = newLine + ' and hits ' + event['damage'].amount.__str__() + ' points of damage'
                self.eventHistory.append(newLine)
            elif event['type'] == 'item':
                if 'pick up' in event.keys():
                    newLine = event['character'].name + ' picks up ' + event['item'].get_name(self.application.world.player)
                    self.eventHistory.append(newLine)
                elif 'drop' in event.keys():
                    newLine = event['character'].name + ' drops ' + event['item'].get_name(self.application.world.player)
                    self.eventHistory.append(newLine)
                elif 'wield' in event.keys():
                    newLine = event['character'].name + ' wields ' + event['item'].get_name(self.application.world.player)
                    if event['proficient'] == False:
                        newLine = newLine + ' but feels uncomfortable with it'
                    self.eventHistory.append(newLine)
                elif 'unwield' in event.keys():
                    newLine = event['character'].name + ' unwields ' + event['item'].get_name(self.application.world.player)
                    self.eventHistory.append(newLine)
            elif event['type'] == 'death':
                newLine = event['character'].name + ' is now dead'
                self.eventHistory.append(newLine)
            elif event['type'] == 'magic heal':
                newLine = event['character'].name + ' feels better'
                self.eventHistory.append(newLine)
            elif event['type'] == 'magic damage':
                newLine = event['character'].name + ' feels worse'
                self.eventHistory.append(newLine)
        #clear short term memory
        del self.application.world.player.short_term_memory[:]

    def formatEventHistory(self):
        """
        Parse through event history and return 5 latests rows for displaying
        @return: list of text
        """
        #parse recent events and make a nice text out of them
        eventText = []
        if len(self.eventHistory) <= 5:
            eventText = self.eventHistory
        else:
            eventText = self.eventHistory[-5:]

        return eventText

    def __full_screen_update(self):
        '''
        Updates full screen
        '''
        player = self.application.world.player
        level = player.level

        player.level.full_update_needed = False
        #TODO: don't call during each and every update
        light_matrix = get_fov_matrix(self.application.world, player, 13)

        self.screen.blit(self.background, (0, 0))
        #TODO: make more generic and clean up
        sy = 0
        for y in range(player.location[1] - 9, player.location[1] + 10):
            sx = 0
            for x in range(player.location[0] - 12, player.location[0] + 13):
                #draw floor and walls
                if x >= 0 and y >= 0 and x <= len(level.floor)-1 and y <= len(level.floor[x])-1:
                    tile = self.surface_manager.getIcon(level.floor[x][y])
                    self.screen.blit(tile, (sx * 32, sy * 32 - 8))
                    if not level.walls[x][y] == pyherc.data.tiles.WALL_EMPTY:
                        tile = self.surface_manager.getIcon(level.walls[x][y])
                        self.screen.blit(tile, (sx * 32, sy * 32 - 8))
                    if light_matrix[x][y] == False:
                        tile = self.surface_manager.getIcon(pyherc.data.tiles.FLOOR_EMPTY)
                        self.screen.blit(tile, (sx * 32, sy * 32 - 8))
                else:
                    #draw empty
                    tile = self.surface_manager.getIcon(pyherc.data.tiles.FLOOR_EMPTY)
                    self.screen.blit(tile, (sx * 32, sy * 32 - 8))
                sx = sx + 1
            sy = sy + 1
            sx = 0

        #draw portals
        for item in level.portals:
            x = item.location[0] - player.location[0] + 12
            y = item.location[1] - player.location[1] + 9
            if x >= 0 and y >= 0 and x <= 24 and y <= 14:
                if light_matrix[x + player.location[0] - 12][y + player.location[1] - 9] == True:
                    tile = self.surface_manager.getIcon(item.icon)
                    self.screen.blit(tile, (x * 32, y *32 - 8))

        #draw items
        for item in level.items:
            x = item.location[0] - player.location[0] + 12
            y = item.location[1] - player.location[1] + 9
            if x >= 0 and y >= 0 and x <= 24 and y <= 14:
                if light_matrix[x + player.location[0] - 12][y + player.location[1] - 9] == True:
                    tile = self.surface_manager.getIcon(item.icon)
                    self.screen.blit(tile, (x * 32, y *32 - 8))

        #draw creatures
        for item in level.creatures:
            x = item.location[0] - player.location[0] + 12
            y = item.location[1] - player.location[1] + 9
            if x >= 0 and y >= 0 and x <= 24 and y <= 14:
                if light_matrix[x + player.location[0] - 12][y + player.location[1] - 9] == True:
                    tile = self.surface_manager.getIcon(item.icon)
                    self.screen.blit(tile, (x * 32, y *32 - 8))

        #draw overlay event history
        self.screen.blit(self.console, (0, 0))
        eventText = self.formatEventHistory()
        font = pygame.font.Font(None, 12)
        lineNumber = 0
        for line in eventText:
            text = font.render(line, True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.topleft = (5, 5 + lineNumber * 12)
            self.screen.blit(text, textRect)
            lineNumber = lineNumber + 1

        #temporary hp display
        text = font.render('HP: ' + player.get_hp().__str__() +
                           ' / ' + player.get_max_hp().__str__(), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.topleft = (5, 85)
        self.screen.blit(text, textRect)

        tile = self.surface_manager.getIcon(player.icon)
        self.screen.blit(tile, (384, 280))
        pygame.display.update()

    def __partial_screen_update(self):
        '''
        Updates only those portions of the map that have been marked dirty
        '''
        pass

    def __updateDisplay(self):
        """
        Draws this window on screen
        """
        player = self.application.world.player
        level = player.level

        if player.level.full_update_needed == True:
            self.__full_screen_update()
        else:
            self.__partial_screen_update()
