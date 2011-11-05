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
import pyHerc.gui.surfaceManager
import pyHerc.gui.images
import pyHerc.data.model
import pyHerc.data.tiles
import pyHerc.generators.dungeon

from pygame.locals import K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j
from pygame.locals import K_k, K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t
from pygame.locals import K_u, K_v, K_w, K_x, K_y, K_z
from pygame.locals import K_ESCAPE, K_RETURN, K_SPACE

class Inventory:
    """
    Dialog for selecting one or more items from a list
    """

    def __init__(self, application, screen, surface_manager = None):
        """
        Initalises this component
        @param application: link to application showing the display
        @param screen: surface for drawing
        @param surface_manager: object for tile graphics management
        """

        self.logger = logging.getLogger('pyHerc.gui.dialogs.Inventory')
        self.inventory = [] # [{'selected': 1/0, 'item' : Item}]
        self.selected = None
        self.selectCount = 0
        self.application = application
        self.screen = screen
        self.page = 0
        self.running = 1
        self.letters = [chr(x) for x in range(97, 123)]
        self.keymap = {K_a:0, K_b:1, K_c:2, K_d:3, K_e:4, K_f:5, K_g:6, K_h:7, K_i:8, K_j:9,
                                K_k:10, K_l:11, K_m:12, K_n:13, K_o:14, K_p:15, K_q:16, K_r:17,
                                K_s:18, K_t:19, K_u:20, K_v:21, K_w:22, K_x:23, K_y:24, K_z:25}

        self.surface_manager = surface_manager
        if self.surface_manager == None:
            self.logger.warn('Surface manager not specified, defaulting to the system one.')
            self.surface_manager = pyHerc.gui.surfaceManager.SurfaceManager()
            self.surface_manager.loadResources()

        self.background = self.surface_manager.getImage(pyHerc.gui.images.image_inventory_menu)

    def show(self, list, multipleSelections = -1):
        """
        Displays dialog
        @param list: list of items to display
        @param multipleSelections: amount of items user is allowed to select
        @return: list of selected items
        @note: if multipleSelections is not specified, default to amount of items
        """
        if multipleSelections == -1:
            multipleSelections = len(list)

        for item in list:
            self.inventory.append({'selected' : 0, 'item' : item})

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.logger.info('Quit received, exiting')
                    self.application.running = 0
                    self.running = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        for item in self.inventory:
                            item['selected'] = 0
                        self.running = 0
                    if event.key == K_RETURN or event.key == K_SPACE:
                        self.running = 0
                    if event.key in self.keymap.keys():
                        index = self.keymap[event.key] + self.page * 26
                        if index < len(self.inventory):
                            if self.inventory[index]['selected'] == 1:
                                self.inventory[index]['selected'] = 0
                                self.selected = None
                                self.selectCount = self.selectCount - 1
                            else:
                                if multipleSelections > 1:
                                    if self.selectCount < multipleSelections:
                                        self.inventory[index]['selected'] = 1
                                        self.selectCount = self.selectCount + 1
                                else:
                                    self.inventory[index]['selected'] = 1
                                    if self.selected != None:
                                        self.inventory[self.selected]['selected'] = 0
                                        self.selected = index
                                    else:
                                        self.selected = index

            self.__updateScreen()

        returnList = []
        for item in self.inventory:
            if item['selected'] == 1:
                returnList.append(item['item'])

        return returnList

    def __updateScreen(self):
        """
        Draws display on screen
        """
        #font size 16
        #top left = 40, 40
        #TODO: take paging into account
        self.screen.blit(self.background, (0, 0))
        font = pygame.font.Font(None, 18)
        for index in range(0, len(self.inventory)):
            item = self.inventory[index]

            if item['selected'] :
                #TODO: get from configuration in beginning
                colour = (255, 255, 255)
            else:
                colour = (200, 200, 200)

            text = font.render(self.letters[index], True, colour, (0, 0, 0))

            textRect = text.get_rect()
            textRect.topleft = (40, 40 + index*20)
            self.screen.blit(text, textRect)
            text = font.render(item['item'].get_name(self.application.world.player, True), True, colour, (0, 0, 0))
            textRect = text.get_rect()
            textRect.topleft = (60, 40 + index*20)
            self.screen.blit(text, textRect)

        pygame.display.update()

    def sort_items(self, items):
        '''
        Sort items according to their type
        @param items: items to sort
        @returns: list of sorted items
        '''
        if items == None:
            return []

        if len(items) == 0:
            return []

        weapons = [item for item in items if item.get_main_type() == 'weapon']
        potions = [item for item in items if item.get_main_type() == 'potion']
        food = [item for item in items if item.get_main_type() == 'food']

        sorted = []
        sorted.extend(weapons)
        sorted.extend(potions)
        sorted.extend(food)

        return sorted

class EndScreen:

    def __init__(self, application, screen, surface_manager = None):
        self.logger = logging.getLogger('pyHerc.gui.dialogs.EndScreen')
        self.background = None
        self.running = 1
        self.application = application
        self.screen = screen
        self.surface_manager = surface_manager
        if self.surface_manager == None:
            self.logger.warn('Surface manager not specified, defaulting to the system one.')
            self.surface_manager = pyHerc.gui.surfaceManager.SurfaceManager()
            self.surface_manager.loadResources()

    def show(self, ending):
        self.logger.info('showing the end screen')
        self.logger.debug(ending)

        font = pygame.font.Font(None, 18)
        colour = (255, 255, 255)
        model = self.application.world
        player = model.player

        if ending['reason'] == 'escaped':
            self.background = self.surface_manager.getImage(pyHerc.gui.images.image_end_marble_slate)
            self.screen.blit(self.background, (0, 0))
            text = font.render(player.name + ' escaped from ruins', True, colour, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (400, 200)
            self.screen.blit(text, textRect)

        elif ending['reason'] == 'victory':
            self.background = self.surface_manager.getImage(pyHerc.gui.images.image_end_marble_slate)
            self.screen.blit(self.background, (0, 0))
            text = font.render(player.name + ' conquered the ruins', True, colour, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (400, 200)
            self.screen.blit(text, textRect)

        elif ending['reason'] == 'dead':
            self.background = self.surface_manager.getImage(pyHerc.gui.images.image_end_tombstone)
            self.screen.blit(self.background, (0, 0))
            text = font.render(player.name + ' died in ruins', True, colour, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (400, 200)
            self.screen.blit(text, textRect)
            text = font.render(ending['dead reason'], True, colour, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (400, 220)
            self.screen.blit(text, textRect)
        else:
            #quit
            self.background = self.surface_manager.getImage(
                                                                 pyHerc.gui.images.image_end_marble_slate)
            self.screen.blit(self.background, (0, 0))
            text = font.render(player.name + ' quit', True, colour, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (400, 200)
            self.screen.blit(text, textRect)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.logger.info('Quit received, exiting')
                    self.application.running = 0
                    self.running = 0
                if event.type == pygame.KEYDOWN:
                    if event.key in (K_ESCAPE, K_RETURN, K_SPACE):
                        self.running = 0

            self.__updateScreen()

    def __updateScreen(self):
        pygame.display.update()
