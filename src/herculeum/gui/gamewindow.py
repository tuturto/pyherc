#!/usr/bin/env python
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
from pgu.gui import TextArea
import pgu.gui.basic
from pygame import Rect

from pygame.locals import K_ESCAPE
from pygame.locals import K_i
from pygame.locals import K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9

import pygame
import pyherc
import herculeum.config.tiles
from pyherc.rules.los import get_fov_matrix


class GameWindow(Container):
    """
    Container for Game window

    .. versionadded:: 0.4
    """

    def __init__(self,  application, surface_manager, **params):
        """
        Initialises game window

        Args:
            application: instance of currently running application
            screen: display to draw onto
            surface_manager: SurfaceManager for graphics
        """
        super(GameWindow, self).__init__(**params)

        self.play_area = None
        self.text_console = None
        self.lines = []
        self.event_types_to_show = ['attack hit',
                                    'poison triggered',
                                    'poison ended',
                                    'poisoned']

        self.application = application
        self.surface_manager = surface_manager
        self.set_layout()

    def set_layout(self):
        """
        Set layout of this screen
        """
        self.play_area = GameArea(application = self.application,
                                  surface_manager = self.surface_manager)
        self.application.world.player.register_event_listener(self)
        self.add(self.play_area, 0, 45)
        self.text_console = TextArea(
                     value="You set out to adventure\nIt looks dangerous here\nBe careful",
                     width=800,
                     height=40,
                     size=8,
                     focusable = False,
                     font = pygame.font.Font(None, 12),
                     color = (0, 0, 0))
        self.add(self.text_console, 0, 0)
        self.play_area.focus()

    def run(self):
        """
        Update screen
        """
        pass

    def receive_event(self, event):
        """
        Receive event from event subsystem

        :param event: event to receive
        :type event: Event

        .. versionadded:: 0.4
        """
        self.play_area.receive_event(event)

        if event.event_type in self.event_types_to_show:
            self.lines.append(event.third_person())
            self.lines = self.lines[-4:]

            temp_text = ''
            for line in self.lines:
                temp_text = temp_text + line + '\n'

            self.text_console.value = temp_text

class GameArea(Widget):
    """
    Component to draw game area

    .. versionadded:: 0.4
    """
    def __init__(self, application, surface_manager,  **kwargs):
        """
        Default constructor
        """
        super(GameArea, self).__init__(**kwargs)
        self.application = application
        self.surface_manager = surface_manager

        self.move_key_map = {K_KP8:1, K_KP9:2, K_KP6:3, K_KP3:4, K_KP2:5,
                             K_KP1:6, K_KP4:7, K_KP7:8, K_KP5:9}
        self.old_location = (0, 0)
        self.dirty_tiles = []
        self.light_matrix = None

    def paint(self, s):
        """
        Paint this widget on given surface

        :param s: surface to paint on
        :type s: Surface
        """
        player = self.application.world.player
        level = player.level

        player.level.full_update_needed = False

        self.light_matrix = get_fov_matrix(self.application.world, player, 13)

        sy = 0
        for y in range(player.location[1] - 9, player.location[1] + 10):
            sx = 0
            for x in range(player.location[0] - 12, player.location[0] + 13):
                #draw floor and walls
                if x >= 0 and y >= 0 and x <= len(level.floor)-1 and y <= len(level.floor[x])-1:
                    tile = self.surface_manager.get_icon(level.floor[x][y])
                    s.blit(tile, (sx * 32, sy * 32 - 8))
                    if not level.walls[x][y] == herculeum.config.tiles.WALL_EMPTY:
                        tile = self.surface_manager.get_icon(level.walls[x][y])
                        s.blit(tile, (sx * 32, sy * 32 - 8))
                    if self.light_matrix[x][y] == False:
                        tile = self.surface_manager.get_icon(herculeum.config.tiles.FLOOR_EMPTY)
                        s.blit(tile, (sx * 32, sy * 32 - 8))
                else:
                    #draw empty
                    tile = self.surface_manager.get_icon(herculeum.config.tiles.FLOOR_EMPTY)
                    s.blit(tile, (sx * 32, sy * 32 - 8))
                sx = sx + 1
            sy = sy + 1
            sx = 0

        #draw portals
        for item in level.portals:
            x = item.location[0] - player.location[0] + 12
            y = item.location[1] - player.location[1] + 9
            if x >= 0 and y >= 0 and x <= 24 and y <= 14:
                if self.light_matrix[x + player.location[0] - 12][y + player.location[1] - 9] == True:
                    tile = self.surface_manager.get_icon(item.icon)
                    s.blit(tile, (x * 32, y *32 - 8))

        #draw items
        for item in level.items:
            x = item.location[0] - player.location[0] + 12
            y = item.location[1] - player.location[1] + 9
            if x >= 0 and y >= 0 and x <= 24 and y <= 14:
                if self.light_matrix[x + player.location[0] - 12][y + player.location[1] - 9] == True:
                    tile = self.surface_manager.get_icon(item.icon)
                    s.blit(tile, (x * 32, y *32 - 8))

        #draw creatures
        for item in level.creatures:
            x = item.location[0] - player.location[0] + 12
            y = item.location[1] - player.location[1] + 9
            if x >= 0 and y >= 0 and x <= 24 and y <= 14:
                if self.light_matrix[x + player.location[0] - 12][y + player.location[1] - 9] == True:
                    tile = self.surface_manager.get_icon(item.icon)
                    s.blit(tile, (x * 32, y *32 - 8))

        tile = self.surface_manager.get_icon(player.icon)
        s.blit(tile, (384, 280))

    def update(self, s):
        # Update the pygame.Surface and return the update rects
        model = self.application.world
        player = model.player
        level = player.level

        if self.old_location != player.location:
            self.old_location = player.location
            self.paint(s)
            return [Rect(0, 0, self.rect.w, self.rect.h)]
        else:
            player = self.application.world.player
            updated_tiles = []

            for update in self.dirty_tiles:
                screen_x = 384 + (update[0] - player.location[0]) * 32
                screen_y = 280 + (update[1] - player.location[1]) * 32

                if screen_x > 0 and screen_x < 768 and screen_y > 0 and screen_y < 568:
                    #do update
                    if self.light_matrix[update[0]][update[1]] == False:
                        tile = self.surface_manager.get_icon(herculeum.config.tiles.FLOOR_EMPTY)
                        s.blit(tile, (screen_x, screen_y))
                    else:
                        tile = self.surface_manager.get_icon(level.get_tile(update[0], update[1]))
                        s.blit(tile, (screen_x, screen_y))

                        #draw portals
                        portal = level.get_portal_at(update)
                        if portal != None:
                            tile = self.surface_manager.get_icon(portal.icon)
                            s.blit(tile, (screen_x, screen_y))
                        #draw items
                        items = level.get_items_at(update)
                        if len(items) > 0:
                            for item in items:
                                tile = self.surface_manager.get_icon(item.icon)
                                s.blit(tile, (screen_x, screen_y))
                        #draw creatures
                        creature = level.get_creature_at(update)
                        if creature != None:
                            tile = self.surface_manager.get_icon(creature.icon)
                            s.blit(tile, (screen_x, screen_y))

                    updated_tiles.append(Rect(screen_x, screen_y,
                                              screen_x+32, screen_y+32))
            return updated_tiles

    def event(self, event):
        # Handle the pygame.Event
        model = self.application.world
        player = model.player

        if player.tick > 0:
            return

        if event != None:
            if event.type == pygame.QUIT:
                self.application.running = 0
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    #quit
                    self.application.world.end_condition = 1
                elif event.key in self.move_key_map.keys():
                    player.level.full_update_needed = True
                    #handle moving
                    direction = self.move_key_map[event.key]
                    if player.is_move_legal(direction, 'walk'):
                        player.move(direction)
                    else:
                        player.perform_attack(direction)
                elif event.key == K_i:
                    #display inventory
                    self.application.change_state('inventory')

    def resize(self, width=None, height=None):
        # Return the width and height of this widget
        return 800, 600

    def receive_event(self, event):
        """
        Receive event from event subsystem

        :param event: event to receive
        :type event: Event
        """
        assert event != None
        self.dirty_tiles.extend(event.affected_tiles)


