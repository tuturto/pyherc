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
Module for inventory menu related functionality
"""

import pygame
import pgu.gui

from pygame.locals import K_ESCAPE

class InventoryWindow(pgu.gui.Container):
    """
    Inventory window

    .. versionadded:: 0.4
    """

    def __init__(self,  application, surface_manager, **params):
        """
        Initialises inventory menu

        :param application: instance of currently running application
        :type application: Application
        """
        super(InventoryWindow, self).__init__(**params)

        self.running = 1
        self.selection = 0
        self.application = application
        self.surface_manager = surface_manager
        self.set_layout()

    def set_layout(self):
        """
        Set layout of this screen
        """
        pass

    def event(self, event):
        if event != None:
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.application.change_state('game window')
