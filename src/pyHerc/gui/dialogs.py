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
import pyHec.data.model
import pyHec.data.tiles
import pyHec.generators.dungeon

from pygame.locals import *

class ListSelector:
    """
    Dialog for selecting one or more items from a list
    """

    def __init__(self, application, display):
        """
        Initalises this component
        Parameters:
            application : link to application showing the display
            display : surface for drawing
        """
        self.logger = logging.getLogger('pyHerc.gui.dialogs.ListSelector')
        pass

    def show(self, list, parameters):
        """
        Displays dialog
        Parameters:
            list : list of items to display
            parameters : parameters to control the display
        Returns:
            list of selected items
        """
        pass

    def __updateScreen(self):
        """
        Draws display on screen
        Remark:
            Does not update area outside of the display
        """
        pass
