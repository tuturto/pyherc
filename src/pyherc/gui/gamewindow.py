#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
Module main display
"""

from pgu.gui import Widget
from pgu.gui import Container
from pygame import Rect

import pygame
import pyherc
from pyherc.rules.los import get_fov_matrix

class GameWindow(Container):

    def __init__(self,  application, surface_manager, **params):
        """
        Initialises game window

        Args:
            application: instance of currently running application
            screen: display to draw onto
            surface_manager: SurfaceManager for graphics
        """
        super(GameWindow, self).__init__(**params)

        self.application = application
        self.surface_manager = surface_manager
        self.set_layout()

    def set_layout(self):
        """
        Set layout of this screen
        """
        play_area = GameArea(self.application, self.surface_manager)
        self.add(play_area, 0, 0)

    def run(self):
        """
        Update screen
        """
        pass

class GameArea(Widget):
    """
    Component to draw game area
    """
    def __init__(self, application, surface_manager,  **kwargs):
        """
        Default constructor
        """
        super(GameArea, self).__init__(**kwargs)
        self.application = application
        self.surface_manager = surface_manager

    def paint(self,s):
        # Paint the pygame.Surface
        player = self.application.world.player
        level = player.level

        player.level.full_update_needed = False

        light_matrix = get_fov_matrix(self.application.world, player, 13)

        #s.blit(self.background, (0, 0))

        sy = 0
        for y in range(player.location[1] - 9, player.location[1] + 10):
            sx = 0
            for x in range(player.location[0] - 12, player.location[0] + 13):
                #draw floor and walls
                if x >= 0 and y >= 0 and x <= len(level.floor)-1 and y <= len(level.floor[x])-1:
                    tile = self.surface_manager.get_icon(level.floor[x][y])
                    s.blit(tile, (sx * 32, sy * 32 - 8))
                    if not level.walls[x][y] == pyherc.data.tiles.WALL_EMPTY:
                        tile = self.surface_manager.get_icon(level.walls[x][y])
                        s.blit(tile, (sx * 32, sy * 32 - 8))
                    if light_matrix[x][y] == False:
                        tile = self.surface_manager.get_icon(pyherc.data.tiles.FLOOR_EMPTY)
                        s.blit(tile, (sx * 32, sy * 32 - 8))
                else:
                    #draw empty
                    tile = self.surface_manager.get_icon(pyherc.data.tiles.FLOOR_EMPTY)
                    s.blit(tile, (sx * 32, sy * 32 - 8))
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
                    s.blit(tile, (x * 32, y *32 - 8))

        #draw items
        for item in level.items:
            x = item.location[0] - player.location[0] + 12
            y = item.location[1] - player.location[1] + 9
            if x >= 0 and y >= 0 and x <= 24 and y <= 14:
                if light_matrix[x + player.location[0] - 12][y + player.location[1] - 9] == True:
                    tile = self.surface_manager.get_icon(item.icon)
                    s.blit(tile, (x * 32, y *32 - 8))

        #draw creatures
        for item in level.creatures:
            x = item.location[0] - player.location[0] + 12
            y = item.location[1] - player.location[1] + 9
            if x >= 0 and y >= 0 and x <= 24 and y <= 14:
                if light_matrix[x + player.location[0] - 12][y + player.location[1] - 9] == True:
                    tile = self.surface_manager.get_icon(item.icon)
                    s.blit(tile, (x * 32, y *32 - 8))

        #draw overlay event history
        #self.screen.blit(self.console, (0, 0))
        #eventText = self.format_event_history()
        font = pygame.font.Font(None, 12)
        #lineNumber = 0
        #for line in eventText:
        #    text = font.render(line, True, (255, 255, 255))
        #    textRect = text.get_rect()
        #    textRect.topleft = (5, 5 + lineNumber * 12)
        #    self.screen.blit(text, textRect)
        #    lineNumber = lineNumber + 1

        #temporary hp display
        text = font.render('HP: ' + str(player.hit_points) +
                           ' / ' + str(player.max_hp), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.topleft = (5, 85)
        s.blit(text, textRect)

        tile = self.surface_manager.get_icon(player.icon)
        s.blit(tile, (384, 280))

    def update(self,s):
        # Update the pygame.Surface and return the update rects
        self.paint(s)
        return [Rect(0,0,self.rect.w,self.rect.h)]

    def event(self,e):
        # Handle the pygame.Event
        return

    def resize(self,width=None,height=None):
        # Return the width and height of this widget
        return 800, 600
