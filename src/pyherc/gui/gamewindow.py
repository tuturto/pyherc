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
        return

    def update(self,s):
        # Update the pygame.Surface and return the update rects
        return [Rect(0,0,self.rect.w,self.rect.h)]

    def event(self,e):
        # Handle the pygame.Event
        return

    def resize(self,width=None,height=None):
        # Return the width and height of this widget
        return 256,256
