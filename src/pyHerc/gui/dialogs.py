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
import pyHerc.data.model
import pyHerc.data.tiles
import pyHerc.generators.dungeon

from pygame.locals import *

class Inventory:
    """
    Dialog for selecting one or more items from a list
    """

    def __init__(self, application, screen):
        """
        Initalises this component
        Parameters:
            application : link to application showing the display
            screen : surface for drawing
        """
        assert(application != None)
        assert(screen != None)

        self.logger = logging.getLogger('pyHerc.gui.dialogs.Inventory')
        self.inventory = [] # [{'selected': 1/0, 'item' : Item}]
        self.selected = None
        self.application = application
        self.screen = screen
        self.page = 0
        self.running = 1
        self.letters = map(chr, range(97, 123))
        self.keymap = {K_a:0, K_b:1, K_c:2, K_d:3, K_e:4, K_f:5, K_g:6, K_h:7, K_i:8, K_j:9,
                                K_k:10, K_l:11, K_m:12, K_n:13, K_o:14, K_p:15, K_q:16, K_r:17,
                                K_s:18, K_t:19, K_u:20, K_v:21, K_w:22, K_x:23, K_y:24, K_z:25}

        self.background = surfaceManager.getImage(images.image_inventory_menu)

    def show(self, list, multipleSelections = 1):
        """
        Displays dialog
        Parameters:
            list : list of items to display
            multipleSelections : is user allowed to select multiple items
        Returns:
            list of selected items
        """
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
                            else:
                                self.inventory[index]['selected'] = 1
                                if multipleSelections == 0:
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
            text = font.render(item['item'].name, True, colour, (0, 0, 0))
            textRect = text.get_rect()
            textRect.topleft = (60, 40 + index*20)
            self.screen.blit(text, textRect)

        pygame.display.update()
