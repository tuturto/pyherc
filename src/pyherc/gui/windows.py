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
from pyherc.aspects import Logged
from pyherc.rules.public import MoveParameters
from pyherc.rules.public import AttackParameters
from pyherc.rules.los import get_fov_matrix
from pygame.locals import K_ESCAPE, K_PERIOD
from pygame.locals import K_d, K_w, K_r, K_q,  K_i
from pygame.locals import K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9

from pyherc.gui.options import OptionsMenu
from pyherc.gui.startmenu import StartMenu

class MainWindow(pgu.gui.app.App):
    """
    Main window of the game
    """
    logged = Logged()

    @logged
    def __init__(self,  application, base_path, surface_manager, screen, theme=None, **params):
        """
        Initialises the main window

        Args:
            application: instance of currently running application
            base_path: location of resources directory
            surface_manager: optional SurfaceManger to use for loading resources
        """
        super(MainWindow, self).__init__(theme, **params)
        self.logger = logging.getLogger('pyherc.gui.windows.MainWindow')
        self.logger.info('Initialising MainWindow')
        self.display = None
        self.application = application
        pygame.init()
        self.width = application.config.resolution[0]
        self.height = application.config.resolution[1]
        self.screen = screen
        pygame.display.set_caption(application.config.caption)

        self.surface_manager = surface_manager

    @logged
    def change_state(self, state):
        """
        Change state of the gui

        Args:
            state: String specifying which state to display
        """
        if state == 'options menu':
            mode = OptionsMenu(self.application,
                               self.screen,
                               self.surface_manager)
        elif state == 'start menu':
            mode = StartMenu(self.application,
                             self.screen,
                             self.surface_manager)

        if state != None:
            self.init(widget = mode, screen = self.screen)



class StartNewGameWindow:
    """
    Window that is displayed when player starts a new game
    """
    def __init__(self,  application, screen, surface_manager):
        self.logger = logging.getLogger('pyherc.gui.windows.StartNewGameWindow')

        self.running = 1
        self.application = application
        self.screen = screen
        self.surface_manager = surface_manager
        self.character = None

    def main_loop(self):
        """
        Main loop of the window
        """
        self.__generate_new_game()

    def __generate_new_game(self):
        """
        Generate a new game
        """
        self.character = pyherc.rules.character.create_character('human',
                                                'fighter',
                                                self.application.world,
                                                self.application.action_factory,
                                                self.application.rng)
        self.application.world.player = self.character

        level_generator = self.application.level_generator_factory.get_generator('upper catacombs')

        generator = pyherc.generators.dungeon.DungeonGenerator(
                                self.application.creature_generator,
                                self.application.item_generator,
                                level_generator)

        generator.generate_dungeon(self.application.world)
        self.character.level = self.application.world.dungeon.levels
        self.character.name = 'Adventurer'

class GameWindow:
    """
    Window that displays the playing world
    """
    logged = Logged()

    @logged
    def __init__(self,  application, screen, surface_manager):
        self.logger = logging.getLogger('pyherc.gui.windows.GameWindow')

        self.application = application
        self.screen = screen
        self.fullUpdate = 1
        self.surface_manager = surface_manager
        self.background = self.surface_manager.get_image(images.image_play_area)
        self.console = self.surface_manager.get_image(images.image_console)
        self.moveKeyMap = {K_KP8:1, K_KP9:2, K_KP6:3, K_KP3:4, K_KP2:5, K_KP1:6,
                                    K_KP4:7, K_KP7:8, K_KP5:9}
        self.eventHistory = []

    def __handle_player_input(self):
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
                        if player.is_move_legal(direction, 'walk'):
                            player.move(direction)
                        else:
                            player.perform_attack(direction)
                    elif event.key == K_PERIOD:
                        #pick up items
                        items = player.level.get_items_at(player.location)
                        if len(items) > 1:
                            dialog = dialogs.Inventory(self.application,
                                                       self.screen,
                                                       self.surface_manager,
                                                       player)
                            items = dialog.show(items)
                        for item in items:
                            pyherc.rules.items.pick_up(model, player, item)
                        player.level.full_update_needed = True
                    elif event.key == K_i:
                        #display inventory
                        dialog = dialogs.Inventory(self.application,
                                                   self.screen,
                                                   self.surface_manager,
                                                   player)
                        dialog.show(player.inventory, 0)
                        player.level.full_update_needed = True
                    elif event.key == K_d:
                        #drop items
                        dialog = dialogs.Inventory(self.application,
                                                   self.screen,
                                                   self.surface_manager,
                                                   player)
                        dropItems = dialog.show(player.inventory)
                        for item in dropItems:
                            pyherc.rules.items.drop(model, player, item)
                        player.level.full_update_needed = True
                    elif event.key == K_w:
                        #wield weapons
                        dialog = dialogs.Inventory(self.application,
                                                   self.screen,
                                                   self.surface_manager,
                                                   player)
                        wieldItems = dialog.show(player.inventory, 2)
                        for item in wieldItems:
                            pyherc.rules.items.wield(model, player, item, True)
                        player.level.full_update_needed = True
                    elif event.key == K_r:
                        #unwield weapons
                        dialog = dialogs.Inventory(self.application,
                                                   self.screen,
                                                   self.surface_manager,
                                                   player)
                        removable = dialog.show(player.weapons)
                        for item in removable:
                            pyherc.rules.items.unwield(model, player, item)
                        player.level.full_update_needed = True
                    elif event.key == K_q:
                        #quaff potion
                        dialog = dialogs.Inventory(self.application,
                                                   self.screen,
                                                   self.surface_manager,
                                                   player)
                        potion = dialog.show(player.inventory, 1)
                        if len(potion) == 1:
                            player.drink(potion[0])
                        player.level.full_update_needed = True
            else:
                return

    def main_loop(self):
        """
        Main loop of the game
        """
        while self.application.world.end_condition == 0 and self.application.running:

            model = self.application.world

            creature = pyherc.rules.time.get_next_creature(model)

            if creature == model.player:
                if self.application.world.player.level != None:
                    self.__updateDisplay()
                self.__handle_player_input()
                self.get_new_events()
                if self.application.world.player.level != None:
                    self.__updateDisplay()
            else:
                if self.application.world.player.level != None:
                    creature.act(self.application.world)
                    self.get_new_events()
                    self.application.world.player.level.full_update_needed = True

    def get_new_events(self):
        """
        Process memory of player character and store interesting events
        """
        for event in self.application.world.player.short_term_memory:
            if event['type'] == 'melee':
                newLine = event['attacker'].name + ' attacks'
                if event['hit'] == 0:
                    newLine = newLine + ' but misses'
                else:
                    newLine = newLine + ' and hits ' + str(event['damage'].damage) + ' points of damage'
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

    @logged
    def format_event_history(self):
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

        light_matrix = get_fov_matrix(self.application.world, player, 13)

        self.screen.blit(self.background, (0, 0))

        sy = 0
        for y in range(player.location[1] - 9, player.location[1] + 10):
            sx = 0
            for x in range(player.location[0] - 12, player.location[0] + 13):
                #draw floor and walls
                if x >= 0 and y >= 0 and x <= len(level.floor)-1 and y <= len(level.floor[x])-1:
                    tile = self.surface_manager.get_icon(level.floor[x][y])
                    self.screen.blit(tile, (sx * 32, sy * 32 - 8))
                    if not level.walls[x][y] == pyherc.data.tiles.WALL_EMPTY:
                        tile = self.surface_manager.get_icon(level.walls[x][y])
                        self.screen.blit(tile, (sx * 32, sy * 32 - 8))
                    if light_matrix[x][y] == False:
                        tile = self.surface_manager.get_icon(pyherc.data.tiles.FLOOR_EMPTY)
                        self.screen.blit(tile, (sx * 32, sy * 32 - 8))
                else:
                    #draw empty
                    tile = self.surface_manager.get_icon(pyherc.data.tiles.FLOOR_EMPTY)
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
                    tile = self.surface_manager.get_icon(item.icon)
                    self.screen.blit(tile, (x * 32, y *32 - 8))

        #draw items
        for item in level.items:
            x = item.location[0] - player.location[0] + 12
            y = item.location[1] - player.location[1] + 9
            if x >= 0 and y >= 0 and x <= 24 and y <= 14:
                if light_matrix[x + player.location[0] - 12][y + player.location[1] - 9] == True:
                    tile = self.surface_manager.get_icon(item.icon)
                    self.screen.blit(tile, (x * 32, y *32 - 8))

        #draw creatures
        for item in level.creatures:
            x = item.location[0] - player.location[0] + 12
            y = item.location[1] - player.location[1] + 9
            if x >= 0 and y >= 0 and x <= 24 and y <= 14:
                if light_matrix[x + player.location[0] - 12][y + player.location[1] - 9] == True:
                    tile = self.surface_manager.get_icon(item.icon)
                    self.screen.blit(tile, (x * 32, y *32 - 8))

        #draw overlay event history
        self.screen.blit(self.console, (0, 0))
        eventText = self.format_event_history()
        font = pygame.font.Font(None, 12)
        lineNumber = 0
        for line in eventText:
            text = font.render(line, True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.topleft = (5, 5 + lineNumber * 12)
            self.screen.blit(text, textRect)
            lineNumber = lineNumber + 1

        #temporary hp display
        text = font.render('HP: ' + str(player.hit_points) +
                           ' / ' + player.get_max_hp().__str__(), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.topleft = (5, 85)
        self.screen.blit(text, textRect)

        tile = self.surface_manager.get_icon(player.icon)
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

